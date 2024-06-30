import streamlit as st
from pages.common.fileselector import multi_folder_select
import pandas as pd
from pages.common.graph_util import bar_util
import os
from config import output_dir

filename = "costs_itemized.csv"
choosed_output_list, choosed_abspath_list = multi_folder_select(output_dir)

if choosed_output_list:

    df_list = []
    for abspath in choosed_abspath_list:
        fname = os.path.join(abspath, filename)
        df = pd.read_csv(fname)
        df["Component"] = ['二氧化碳排放成本', '燃料成本', '机组可变运维成本', '本地输配电成本', '旋转储备成本', '电动汽车充电桩运维成本', '储能投资成本', '储能固定运维成本', '储能可变运维成本', '机组固定投资运维成本', '电动汽车充电桩投资成本', '机组启动成本', '传输线路资本成本', '传输线路固定运维成本', '弃风弃光惩罚成本']
        df_list.append(df)
        

    item_list = list(df["Component"])
    # item_list

    total_cost_list = []
    
    option_list = []
    for i, item in enumerate(item_list):
        option = bar_util.create_bar_option(len(choosed_output_list), choosed_output_list)
        value_list = []
        for df in df_list:
            value_list.append(list(df["AnnualCost_Real"].astype(int))[i])
    
        total_cost_list.append(value_list)
        bar_util.add_compare_value(option, item, value_list)
        option_list.append(option)
    
    costdf = pd.DataFrame(total_cost_list)
    sumdf = costdf.sum(axis=0)
    option = bar_util.create_bar_option(len(choosed_output_list), choosed_output_list)
    bar_util.add_compare_value(option, "总成本", list(sumdf))
    st.header("总成本")
    bar_util.plot_option(option, bignum=True)
    
    for item, option in zip(item_list, option_list):
        st.header(item)
        bar_util.plot_option(option, bignum=True)
    
    showdf = st.sidebar.checkbox("展示数据", False)
    if showdf:
        st.header("表格数据")
        costdf.index = item_list
        costdf.loc["总成本"] = list(sumdf)
        costdf.columns = choosed_output_list
        st.dataframe(costdf)
        