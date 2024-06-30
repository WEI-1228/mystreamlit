import pandas as pd
import streamlit as st
import os

from config import output_dir
from pages.common.fileselector import multi_folder_select
from pages.common.graph_util import bar_util

choosed_output_list, choosed_abspath_list = multi_folder_select(output_dir)

if choosed_output_list:
    station_list = None

    options = bar_util.create_bar_option(len(choosed_output_list), choosed_output_list)
    df_list = []
    for abspath in choosed_abspath_list:
        filename = os.path.join(abspath, "BuildStation.csv")
        df = pd.read_csv(filename)
        df_list.append(df)
        if not station_list:
            station_list = list(df["STA_BLD_YRS_1"])

    selected_zone = st.selectbox("选择区域", station_list)
    value_list = []
    for df in df_list:
        value = int(df.loc[df["STA_BLD_YRS_1"] == selected_zone]["BuildStation"])
        value_list.append(value)

    bar_util.add_compare_value(options, "充电桩数量", value_list)
    st.header("充电桩数量对比")
    bar_util.plot_option(options)

