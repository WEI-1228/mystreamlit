import streamlit as st
import os
import pandas as pd
from pages.common.graph_util import line_util
from pages.common.fileselector import single_folder_select
from config import output_dir

folder = single_folder_select(output_dir)

df = pd.read_csv(os.path.join(output_dir, folder, "DispatchSlackUp.csv"))

zone_set = set()
energy_set = set()
tps_set = set()
year_set = set()
hour_list = []

for gen in list(df["GENERATION_PROJECT"]):
    sp = gen.split('-')
    zone_set.add(sp[0])
    energy_set.add(sp[1])
    year_set.add(sp[2])

zone_set = list(zone_set)
zone_set.sort()

energy_set = list(energy_set)
energy_set.sort()

year_set = list(year_set)
year_set.sort()

for tps in list(df["timepoints"]):
    tps_set.add(tps[:-2])
    hour_list.append(int(tps[-2:]))

tps_set = list(tps_set)
tps_set.sort()

zone_col, year_col, tps_col, energy_col = st.columns(4)

zone_selected = zone_col.selectbox(
    '省份',
     zone_set)

year_selected = year_col.selectbox(
    "年份",
    year_set
)

time_selected = tps_col.selectbox(
    '日期',
     tps_set)

energy_selected = energy_col.selectbox(
    '能源',
     ["全部展示"] + energy_set)

show = st.sidebar.checkbox("展示原始数据", False)

df = df.loc[(df["GENERATION_PROJECT"].str.contains(zone_selected)) & (df["GENERATION_PROJECT"].str.contains(year_selected))]

df = df.loc[df["timepoints"].str.contains(time_selected)]

option = line_util.create_line_option(list(range(0, 24, 4)))
if energy_selected == "全部展示":
    show_list = []
    for e in energy_set:
        tmpdf = df.loc[df["GENERATION_PROJECT"] == f"{zone_selected}-{e}-{year_selected}"]
        show_list.append((e, tmpdf))
        merge = list(tmpdf["dispatch_slack_up"])
        
        if len(merge) > 0:
            line_util.add_line(option, e, list(merge))
    line_util.plot_option(option)
    if show:
        st.write("侧边栏可以选择某一种类型，方便查看原始数据")
        show_selected = st.sidebar.selectbox("选择查看的能源类型", ["全部"] + energy_set)
        for e, t in show_list:
            if show_selected == "全部" or show_selected == e:
                st.header(e)
                t
else:
    tmpdf = df.loc[df["GENERATION_PROJECT"] == f"{zone_selected}-{energy_selected}-{year_selected}"]
    merge = list(tmpdf["dispatch_slack_up"])
    if len(merge) > 0:
        line_util.add_line(option, energy_selected, list(merge))
    line_util.plot_option(option)
    if show:
        tmpdf
