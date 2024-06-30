import streamlit as st
from pages.common.fileselector import single_folder_select
from config import output_dir
import os
import pandas as pd

st.set_page_config(page_title="展示页面")

file_list = os.listdir(output_dir)
output_list = []
for file in file_list:
    if os.path.isdir(os.path.join(output_dir, file)) and (file.startswith("input") or file.startswith("output")):
        output_list.append(file)
output_list.sort()
st.header("选择观察文件夹")
item_selected = st.selectbox(
    '选择文件夹',
    output_list)

absfolder = os.path.join(output_dir, item_selected)

file_list = os.listdir(absfolder)
file_list = [x for x in file_list]
file_list.sort()
st.header("选择你想查看的文件")
csv_selected = st.selectbox(
    '选择csv',
     file_list)

if csv_selected.endswith(".csv"):
    df = pd.read_csv(os.path.join(absfolder, csv_selected))
    st.dataframe(df)