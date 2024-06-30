import streamlit as st
import os
import pandas as pd
from pages.common.graph_util.stackbar_total_util import CompareTwoStackBar
from pages.common.fileselector import multi_folder_select
from config import output_dir

choosed_output_list, choosed_abspath_list = multi_folder_select(output_dir)

if choosed_output_list:
    df_list = []
    for output in choosed_abspath_list:
        file = os.path.join(output, "DispatchGen.csv")
        df = pd.read_csv(file)
        df_list.append(df)

    zone_set = set()
    energy_set = set()
    tps_set = set()
    hour_set = set()

    for gen in list(df["GEN_TPS_1"]):
        sp = gen.split('-')
        zone_set.add(sp[0])
        energy_set.add(sp[1])

    zone_set = list(zone_set)
    zone_set.sort()

    energy_set = list(energy_set)
    energy_set.sort()
    energy_set.insert(0, energy_set[-1])
    energy_set.insert(0, energy_set[-2])
    del energy_set[-1]
    del energy_set[-1]
    
    for tps in list(df["GEN_TPS_2"]):
        tps_set.add(tps[:-2])
        hour_set.add(tps[-2:])


    tps_set = list(tps_set)
    tps_set.sort()

    hour_set = list(hour_set)
    hour_set.sort()

    zone_col, tps_col, hour_col = st.columns(3)

    zone_selected = zone_col.selectbox(
        '省份',
        zone_set)

    time_selected = tps_col.selectbox(
        '日期',
        tps_set)

    hour_selected = hour_col.selectbox(
        '时间',
        hour_set)

    stack = CompareTwoStackBar(choosed_output_list)
    for energy in energy_set:
        value_list = []
        for df in df_list:
            df = df.loc[df["GEN_TPS_1"].str.startswith(f"{zone_selected}-{energy}")]
            df = df.loc[df["GEN_TPS_2"] == time_selected + hour_selected]
            value_list.append(int(df["DispatchGen"].sum()))
        stack.add_part(energy, value_list)
    
    html = stack.export_html()
    # st.text(html)
    st.components.v1.html(html, height=700)
    
    if st.sidebar.checkbox("展示原始数据", False):
        df = pd.DataFrame(stack.export_df())
        df.index = energy_set
        df.columns = choosed_output_list
        df
    