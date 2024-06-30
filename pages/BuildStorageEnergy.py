import streamlit as st
import os
from pages.common.graph_util import bar_util
import pandas as pd
from streamlit_echarts import st_echarts
from pages.common.fileselector import multi_folder_select
from config import output_dir

choosed_output_list, choosed_abspath_list = multi_folder_select(output_dir)

if choosed_output_list:

    df_list = []
    for output in choosed_abspath_list:
        df = pd.read_csv(os.path.join(output, "BuildStorageEnergy.csv"))
        df_list.append(df)

    storage_list = list(df["STR_BLD_YRS_1"])
    zone_list = set()
    for storage in storage_list:
        if storage.find("-Battery") != -1:
            sp = storage.split('-')
            zone_list.add(sp[0])
    zone_list = list(zone_list)
    zone_list.sort()

    year_list = list(set(df["STR_BLD_YRS_2"]))


    zone_col, year_col = st.columns(2)

    zone_selected = zone_col.selectbox(
        '省份',
        zone_list)

    year_selected = year_col.selectbox(
        '日期',
        year_list)

    data1_list = []
    data2_list = []
    data3_list = []
    for df in df_list:
        df = df.loc[df["STR_BLD_YRS_2"] == year_selected]
        df = df.loc[df["STR_BLD_YRS_1"].str.contains(zone_selected)]
        value_list = list(df["BuildStorageEnergy"])
        data1_list.append(value_list[0])
        data2_list.append(value_list[1])
        data3_list.append(value_list[2])
        
    option = bar_util.create_bar_option(len(choosed_output_list), choosed_output_list)
    bar_util.add_compare_value(option, "新能源配储", data1_list)
    bar_util.add_compare_value(option, "电网侧储能", data2_list)
    bar_util.add_compare_value(option, "用户侧储能", data3_list)
    bar_util.plot_option(option, danwei="kw")
