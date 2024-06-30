from streamlit_echarts import st_echarts
import streamlit as st

def create_line_option(xlabel, useDataZoon=False):
    """
    xlabel: x轴的标签，必须是数值
    """
    option = {
        "xAxis": {
            "type": 'category',
            "data": xlabel
        },
        "yAxis": {
            "type": 'value',
            "axisLabel": {
                "formatter": "{value} kw"
            }
        },
        "legend": {
            "data": []
        },
        "tooltip": {
            "trigger": 'axis',
            "axisPointer": {
            "type": 'cross'
            }
        },
        "series": [
        ]
    }
    
    if useDataZoon:
        option["dataZoom"] = [
            {
            "type": 'slider',
            "start": 0,
            "end": 100
            },
            {
            "type": 'inside',
            "start": 0,
            "end": 100
            }
        ]
    
    return option


def add_line(option, name, data):
    x_len = len(option["xAxis"]["data"])
    data_len = len(data)
    if data_len != x_len:
        raise AssertionError(f'x轴长度为 {x_len} 输入数据长度为 {data_len} 不一致')
    series = {
            "name": name,
            "data": data,
            "type": 'line'
    }
    option["series"].append(series)
    option["legend"]["data"].append(name)
    

def plot_option(option, height="400px"):
    st_echarts(
        options=option, height=height,
    )
    

if __name__ == "__main__":
    option = create_line_option(["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"])
    add_line(option, "A", [820, 932, 901, 934, 1290, 1330, 1320])
    add_line(option, "B", [20, 932, 901, 934, 1290, 1330, 1320])
    plot_option(option)