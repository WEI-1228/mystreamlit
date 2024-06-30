import streamlit as st
import pandas as pd
import os
from pages.common import buildgraph
from config import input_dir
from config import output_dir
import copy

st.set_page_config(page_title="传输线路", layout="wide")
file_list = os.listdir(output_dir)
output_list = []
for file in file_list:
    if file.startswith("output") and os.path.isdir(os.path.join(output_dir, file)):
        output_list.append(file)
        

st.header("全国电力传输线路展示")
left_col, mid_col, right_col = st.columns(3)
folder = left_col.selectbox(
'选择输出文件',
    output_list)

df = pd.read_csv(os.path.join(output_dir, folder, "DispatchTx.csv"))
tps = list(df["TRANS_TIMEPOINTS_3"])
day_list = set()
hour_list = set()
for tp in tps:
    day_list.add(tp[:-3])
    hour_list.add(tp[-2:])

day_list = list(day_list)
day_list.sort()
hour_list = list(hour_list)
hour_list.sort()

day = mid_col.selectbox(
'选择日期',
    day_list)

hour = right_col.selectbox(
'选择小时',
    hour_list)

loads_df = pd.read_csv(os.path.join(input_dir, "loads.csv"))
zone_set = list(set(list(loads_df["load_zone"])))
zone_set.sort()
zone_selected = st.selectbox(
'选择中心城市',
    ['全国'] + zone_set)

graph_meta = buildgraph.GraphMeta()

if "cached_graph_meta" not in st.session_state:
    for zone in zone_set:
        v = loads_df.loc[(loads_df["load_zone"] == zone) & (loads_df["TIMEPOINT"] == f"{day}.{hour}")]
        graph_meta.add_node(zone, float(v["zone_demand_mw"]))
    st.session_state["cached_graph_meta"] = copy.deepcopy(graph_meta)
else:
    graph_meta = st.session_state["cached_graph_meta"]
    graph_meta.clean_link()

    
if zone_selected != "全国":
    df = df.loc[(df["TRANS_TIMEPOINTS_1"] == zone_selected) | (df["TRANS_TIMEPOINTS_2"] == zone_selected)]
                
df = df.loc[df["TRANS_TIMEPOINTS_3"] == f"{day}.{hour}"]
df = df.loc[df["DispatchTx"] != 0]

src_list = list(df["TRANS_TIMEPOINTS_1"])
dst_list = list(df["TRANS_TIMEPOINTS_2"])
w_list = list(df["DispatchTx"])

for src, dst, w in zip(src_list, dst_list, w_list):
    graph_meta.link_between(src, dst, w)

graph = graph_meta.export_data()
buildgraph.plot_graph(graph, "全国电力传输路线")

if zone_selected != "全国":
    st.header(f"zone demand mw：{graph_meta.get_value_by_name(zone_selected)}")

st.header("原始数据")
df