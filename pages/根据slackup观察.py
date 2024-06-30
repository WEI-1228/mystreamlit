import pandas as pd
import streamlit as st
import os
from pages.common.graph_util import line_and_pie
from pages.common.graph_util.double_stackbar_util import CompareTwoStackBar

from config import output_dir

st.header("选择展示的输出文件")
left_col, right_col = st.columns(2)
with left_col:
    file_list = os.listdir(output_dir)
    output_list = []
    for file in file_list:
        if file.startswith("output") and os.path.isdir(os.path.join(output_dir, file)):
            output_list.append(file)
            
    folder = st.selectbox(
    '选择输出文件',
     output_list)

slackupdf = pd.read_csv(os.path.join(output_dir, folder, "DispatchSlackUp.csv"))

slackupdf = slackupdf.loc[slackupdf["dispatch_slack_up"] != 0]

slackupdf = slackupdf.loc[(slackupdf["GENERATION_PROJECT"].str.contains("PV")) | (slackupdf["GENERATION_PROJECT"].str.contains("Wind"))].reset_index(drop=True)

slackupdf.index.name = "行号"

slackupdf

if len(slackupdf) == 0:
    exit()
    
# 将三列合并为一个字符串，并用竖线分隔
# options = slackupdf.apply(lambda row: f"{row['GENERATION_PROJECT']} | {row['timepoints']} | {row['dispatch_slack_up']}", axis=1)

# selected_option = st.selectbox("请选择一个选项:", options)

# # 显示选中的选项
# st.write("你选择了:", selected_option)

idx = None
with right_col:
    idx = st.text_input("输入需要观察的行号")

if not idx:
    exit()
idx = int(idx)

if idx not in slackupdf.index:
    st.error(f"行号{idx}不存在")
    exit()
    
selected = list(slackupdf.loc[int(idx)])

zone_selected, energy_selected, year = selected[0].split('-')
time_selected, hour_selected = selected[1][:-2], selected[1][-2:]

############### dispatch_gen ################

dispatchdf = pd.read_csv(os.path.join(output_dir, folder, "DispatchGen.csv"))
energy_set = set()
hour_list = []

new_column_list = []

for gen in list(dispatchdf["GEN_TPS_1"]):
    sp = gen.split('-')
    new_column_list.append(f"{sp[0]}-{sp[1]}")
    
dispatchdf["GEN_TPS_1"] = new_column_list
dispatchdf = dispatchdf.groupby(["GEN_TPS_1", "GEN_TPS_2"]).sum().reset_index()

for gen in list(dispatchdf["GEN_TPS_1"]):
    sp = gen.split('-')
    energy_set.add(sp[1])

for tps in list(dispatchdf["GEN_TPS_2"]):
    hour_list.append(int(tps[-2:]))

dispatchdf["hour"] = hour_list

st.header(f"{zone_selected} {time_selected[:-1]}")

dispatchdf = dispatchdf.loc[dispatchdf["GEN_TPS_1"].str.contains(zone_selected)]
dispatchdf = dispatchdf.loc[dispatchdf["GEN_TPS_2"].str.contains(time_selected)]
option1 = line_and_pie.create_line_option([str(x) for x in list(range(0, 24, 4))])

show_list = []
for e in energy_set:
    tmp_df = dispatchdf.loc[dispatchdf["GEN_TPS_1"].str.contains(f'-{e}')]
    show_list.append((e, tmp_df))
    merge = tmp_df.groupby("hour")["DispatchGen"].mean().astype(int)
    if len(merge) > 0:
        line_and_pie.add_compare_value(option1, e, list(merge))
line_and_pie.plot_option(option1, height=700)

show = st.sidebar.checkbox("展示原始数据", False)
if show:
    st.header("原始数据")
    st.write("侧边栏可以选择某一种类型，方便查看原始数据")
    show_selected = st.sidebar.selectbox("选择查看的能源类型", ["全部"] + list(energy_set))
    for e, t in show_list:
        if show_selected == "全部" or show_selected == e:
            st.header(e)
            st.dataframe(t, hide_index=True)

############### load_zone ################
file1 = os.path.join(output_dir, folder, "load_balance.csv")
file2 = os.path.join(output_dir, folder, "local_td_energy_balance_wide.csv")
df1 = pd.read_csv(file1)
df2 = pd.read_csv(file2)
df1["timestamp"] = df2["timestamp"]

df1_column = list(df1.columns[2:])
df2_column = list(df2.columns[2:])

stackbar = CompareTwoStackBar([folder])

for item in df1_column:
    baseline_list = []
    value = df1.loc[(df1["load_zone"] == zone_selected) & (df1["timestamp"] == time_selected + hour_selected)][item]
    baseline_list.append(float(value))
    stackbar.add_left_part(item, baseline_list)

for item in df2_column:
    baseline_list = []
    value = df2.loc[(df2["load_zone"] == zone_selected) & (df2["timestamp"] == time_selected + hour_selected)][item]
    baseline_list.append(float(value))
    stackbar.add_right_part(item, baseline_list)
    

leftdata, rightdata = stackbar.export_df()
leftdf = pd.DataFrame(leftdata).transpose()
rightdf = pd.DataFrame(rightdata).transpose()
leftcolname = ["中心发电量", "净传输电量", "储能净传输量", "储能放电量", "中心提取量", "储能充电量"]
rightcolname = ["分布发电量", "分布注入量", "用户储能放电量", "EV放电量", "区域负载", "用户储能充电量", "电动汽车充电量"]
leftdf.columns = leftcolname
rightdf.columns = rightcolname

st.header(f"{zone_selected} {time_selected[5:7]}月 {time_selected[8:10]}日 {hour_selected}时")
st.dataframe(leftdf, hide_index=True, )
st.dataframe(rightdf, hide_index=True)