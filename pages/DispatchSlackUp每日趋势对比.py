import streamlit as st
import os
import pandas as pd
from pages.common.graph_util import line_util
from pages.common.fileselector import multi_folder_select
from config import output_dir

choosed_output_list, choosed_abspath_list = multi_folder_select(output_dir)

if choosed_output_list:
    df_list = []
    for output in choosed_abspath_list:
        df = pd.read_csv(os.path.join(output, "DispatchSlackUp.csv"))
        df_list.append(df)

    zone_set = set()
    energy_set = set()
    tps_set = set()
    hour_list = []
    year_set = set()

    for gen in list(df["GENERATION_PROJECT"]):
        sp = gen.split('-')
        zone_set.add(sp[0])
        energy_set.add(sp[1])
        year_set.add(sp[2])
    
    year_set = list(year_set)
    year_set.sort()

    zone_set = list(zone_set)
    zone_set.sort()

    energy_set = list(energy_set)
    energy_set.sort()


    for tps in list(df["timepoints"]):
        tps_set.add(tps[:-2])
        hour_list.append(int(tps[-2:]))

    for df in df_list:
        df["hour"] = hour_list

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
        energy_set)

    show = st.sidebar.checkbox("展示原始数据", False)


    option = line_util.create_line_option(list(range(0, 24, 4)))
    show_list = []
    for df, outputname in zip(df_list, choosed_output_list):
        df = df.loc[df["GENERATION_PROJECT"] == f"{zone_selected}-{energy_selected}-{year_selected}"]

        df = df.loc[df["timepoints"].str.contains(time_selected)]
        
        tmp_df = df.loc[df["GENERATION_PROJECT"].str.contains(f'-{energy_selected}-')]
        show_list.append((outputname, tmp_df))
        merge = tmp_df["dispatch_slack_up"].astype(int)
        line_util.create_line_option(list(range(0, 24, 4)))
        if len(merge) > 0:
            line_util.add_line(option, outputname, list(merge))

    line_util.plot_option(option)

    if show:
        for name, t in show_list:
            st.header(name)
            t