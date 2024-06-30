import streamlit as st
import os
import pandas as pd
from pages.common.graph_util import line_util, line_and_pie
from pages.common.fileselector import single_folder_select
from config import output_dir

folder = single_folder_select(output_dir)

df = pd.read_csv(os.path.join(output_dir, folder, "DispatchGen.csv"))

zone_set = set()
energy_set = set()
tps_set = set()
hour_list = []
new_column_list = []

for gen in list(df["GEN_TPS_1"]):
    sp = gen.split('-')
    new_column_list.append(f"{sp[0]}-{sp[1]}")
    
df["GEN_TPS_1"] = new_column_list

df = df.groupby(["GEN_TPS_1", "GEN_TPS_2"]).sum().reset_index()

for gen in list(df["GEN_TPS_1"]):
    sp = gen.split('-')
    zone_set.add(sp[0])
    energy_set.add(sp[1])

zone_set = list(zone_set)
zone_set.sort()
zone_set.insert(0, "全国平均")

energy_set = list(energy_set)
energy_set.sort()


for tps in list(df["GEN_TPS_2"]):
    tps_set.add(tps[:-2])
    hour_list.append(int(tps[-2:]))

df["hour"] = hour_list

tps_set = list(tps_set)
tps_set.sort()
tps_set.insert(0, "平均")

zone_col, tps_col, energy_col = st.columns(3)

zone_selected = zone_col.selectbox(
    '省份',
     zone_set)

time_selected = tps_col.selectbox(
    '日期',
     tps_set)

energy_selected = energy_col.selectbox(
    '能源',
     ["全部展示", "平均"] + energy_set)

if zone_selected != "全国平均":
    df = df.loc[df["GEN_TPS_1"].str.contains(zone_selected)]

if time_selected != "平均":
    df = df.loc[df["GEN_TPS_2"].str.contains(time_selected)]

show = st.sidebar.checkbox("展示原始数据", False)
option = line_util.create_line_option(list(range(0, 24, 4)))
option1 = line_and_pie.create_line_option([str(x) for x in list(range(0, 24, 4))])
if energy_selected == "全部展示":
    show_list = []
    for e in energy_set:
        tmp_df = df.loc[df["GEN_TPS_1"].str.contains(f"-{e}")]
        show_list.append((e, tmp_df))
        merge = tmp_df.groupby("hour")["DispatchGen"].mean().astype(int)
        if len(merge) > 0:
            line_and_pie.add_compare_value(option1, e, list(merge))
    line_and_pie.plot_option(option1, height=700)
    
    if show:
        st.header("原始数据")
        st.write("侧边栏可以选择某一种类型，方便查看原始数据")
        show_selected = st.sidebar.selectbox("选择查看的能源类型", ["全部"] + energy_set)
        for e, t in show_list:
            if show_selected == "全部" or show_selected == e:
                st.header(e)
                t
        
elif energy_selected == "平均":
    merge = df.groupby("hour")["DispatchGen"].mean()
    if len(merge) > 0:
        line_util.add_line(option, energy_selected, list(merge))
    line_util.plot_option(option)
    if show:
        st.header("原始数据")
        df
else:
    tmp_df = df.loc[df["GEN_TPS_1"].str.contains(f"-{energy_selected}")]
    merge = tmp_df.groupby("hour")["DispatchGen"].mean()
    if len(merge) > 0:
        line_util.add_line(option, energy_selected, list(merge))
    line_util.plot_option(option)
    if show:
        st.header("原始数据")
        tmp_df