import os
import streamlit as st


def multi_folder_select(output_dir, col_num=3):
    file_list = os.listdir(output_dir)
    output_list = []
    for file in file_list:
        if file.startswith("output") and os.path.isdir(os.path.join(output_dir, file)):
            output_list.append(file)
        
    if "choosed_output_list" not in st.session_state:
        st.session_state.choosed_output_list = []
        st.session_state.choosed_abspath_list = []
        
    st.header("选择展示的输出文件")
    cols = st.columns(col_num)
    for i, output in enumerate(output_list):
        with cols[i % col_num]:
            if st.checkbox(output, False):
                if output not in st.session_state.choosed_output_list:
                    st.session_state.choosed_output_list.append(output)
                    st.session_state.choosed_abspath_list.append(os.path.join(output_dir, output))
            else:
                if output in st.session_state.choosed_output_list:
                    st.session_state.choosed_output_list.remove(output)
                    st.session_state.choosed_abspath_list.remove(os.path.join(output_dir, output))
    
    return st.session_state.choosed_output_list, st.session_state.choosed_abspath_list

def single_folder_select(output_dir):
    file_list = os.listdir(output_dir)
    output_list = []
    for file in file_list:
        if file.startswith("output") and os.path.isdir(os.path.join(output_dir, file)):
            output_list.append(file)
            
    st.header("选择展示的输出文件")
    item_selected = st.selectbox(
    '选择输出文件',
     output_list)
    return item_selected