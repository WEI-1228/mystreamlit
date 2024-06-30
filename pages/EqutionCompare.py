import streamlit as st
from pages.common.fileselector import multi_folder_select
from pages.common.graph_util.double_stackbar_util import CompareTwoStackBar
from config import output_dir
import pandas as pd
import os

st.set_page_config(layout="wide")

choosed_output_list, choosed_abspath_list = multi_folder_select(output_dir)

if choosed_abspath_list:

    df1_list = []
    df2_list = []
    for output in choosed_abspath_list:
        file1 = os.path.join(output, "load_balance.csv")
        file2 = os.path.join(output, "local_td_energy_balance_wide.csv")
        df1 = pd.read_csv(file1)
        df2 = pd.read_csv(file2)
        df1["timestamp"] = df2["timestamp"]
        df1_list.append(df1)
        df2_list.append(df2)
        

    zone_set = set()
    tps_set = set()
    hour_list = set()

    for zone in list(df1["load_zone"]):
        zone_set.add(zone)

    zone_set = list(zone_set)
    zone_set.sort()

    for tps in list(df1["timestamp"]):
        tps_set.add(tps[:-2])
        hour_list.add(tps[-2:])

    tps_set = list(tps_set)
    tps_set.sort()

    hour_list = list(hour_list)
    hour_list.sort()

    zone_col, tps_col, hour_col = st.columns(3)

    zone_selected = zone_col.selectbox(
        '省份',
        zone_set)

    time_selected = tps_col.selectbox(
        '日期',
        tps_set)

    hour_selected = hour_col.selectbox(
        '时间',
        hour_list)

    df1_column = list(df1.columns[2:])
    df2_column = list(df2.columns[2:])

    stackbar = CompareTwoStackBar(choosed_output_list)
    
    for item in df1_column:
        baseline_list = []
        for df in df1_list:
            value = df.loc[(df["load_zone"] == zone_selected) & (df["timestamp"] == time_selected + hour_selected)][item]
            baseline_list.append(float(value))
        stackbar.add_left_part(item, baseline_list)

    for item in df2_column:
        baseline_list = []
        for df in df2_list:
            value = df.loc[(df["load_zone"] == zone_selected) & (df["timestamp"] == time_selected + hour_selected)][item]
            baseline_list.append(float(value))
        stackbar.add_right_part(item, baseline_list)
        
    # html = stackbar.export_html()

    # st.components.v1.html(html, height=600)
    
    leftdata, rightdata = stackbar.export_df()
    leftdf = pd.DataFrame(leftdata).transpose()
    rightdf = pd.DataFrame(rightdata).transpose()
    
    leftdf.index = choosed_output_list
    rightdf.index = choosed_output_list
    leftcol, rightcol = st.columns(2)
    leftcolname = ["中心发电量", "净传输电量", "储能净传输量", "储能放电量", "中心提取量", "储能充电量"]
    rightcolname = ["分布发电量", "分布注入量", "用户储能放电量", "EV放电量", "区域负载", "用户储能充电量", "电动汽车充电量"]
    leftdf.columns = leftcolname
    rightdf.columns = rightcolname
    leftcol.dataframe(leftdf)
    rightcol.dataframe(rightdf)