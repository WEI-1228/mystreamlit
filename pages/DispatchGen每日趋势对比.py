import streamlit as st
import os
import pandas as pd
from pages.common.graph_util import line_util
from pages.common.fileselector import single_folder_select, multi_folder_select
from config import output_dir

choosed_output_list, choosed_abspath_list = multi_folder_select(output_dir)

if choosed_output_list:
    df_list = []
    new_column_list = []
    for output in choosed_abspath_list:
        df = pd.read_csv(os.path.join(output, "DispatchGen.csv"))
        if not new_column_list:
            for gen in list(df["GEN_TPS_1"]):
                sp = gen.split('-')
                new_column_list.append(f"{sp[0]}-{sp[1]}")
        
        df["GEN_TPS_1"] = new_column_list
        df = df.groupby(["GEN_TPS_1", "GEN_TPS_2"]).sum().reset_index()  
        
        df_list.append(df)

    zone_set = set()
    energy_set = set()
    tps_set = set()
    hour_list = []

    for gen in list(df["GEN_TPS_1"]):
        sp = gen.split('-')
        zone_set.add(sp[0])
        energy_set.add(sp[1])

    zone_set = list(zone_set)
    zone_set.sort()
    zone_set.insert(0, "全国")

    energy_set = list(energy_set)
    energy_set.sort()
    energy_set.insert(0, "平均")


    for tps in list(df["GEN_TPS_2"]):
        tps_set.add(tps[:-2])
        hour_list.append(int(tps[-2:]))

    for df in df_list:
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
        energy_set)

    show = st.sidebar.checkbox("展示原始数据", False)

    option = line_util.create_line_option(list(range(0, 24, 4)))
    show_list = []
    for df, outputname in zip(df_list, choosed_output_list):
        if zone_selected != "全国":
            df = df.loc[df["GEN_TPS_1"].str.contains(zone_selected)]

        if time_selected != "平均":
            df = df.loc[df["GEN_TPS_2"].str.contains(time_selected)]
        
        if energy_selected == "平均":
            show_list.append((outputname, df))
            merge = df.groupby("hour")["DispatchGen"].mean().astype(int)
            if len(merge) > 0:
                line_util.add_line(option, outputname, list(merge))
        else:
            tmp_df = df.loc[df["GEN_TPS_1"].str.contains(f'-{energy_selected}')]
            show_list.append((outputname, tmp_df))
            merge = tmp_df.groupby("hour")["DispatchGen"].mean().astype(int)
            line_util.create_line_option(list(range(0, 24, 4)))
            if len(merge) > 0:
                line_util.add_line(option, outputname, list(merge))

    line_util.plot_option(option)

    if show:
        for name, t in show_list:
            st.header(name)
            t