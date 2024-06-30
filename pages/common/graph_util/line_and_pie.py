import streamlit as st
import os
import pandas as pd
from pages.common.fileselector import multi_folder_select
from config import output_dir
import json


def create_line_option(baseline_list, smooth=True):
    """
    xlabel: x轴的标签，必须是数值
    """
    baseline_num = len(baseline_list)
    option = {
        "legend": [
            {
               "top": '0%' 
            },
            {
                "bottom": '45%'
            }
        ],
        "tooltip": {
            "trigger": 'axis',
            "showContent": True
        },
        "dataset": {
            "source": [
                ["对比项目"] + baseline_list, 
            ]
        },
        "xAxis": { "type": 'category' },
        "yAxis": { "gridIndex": 0 },
        
        "grid": { "top": '55%' },
        "series": [
        ]
    }
    
    option["series"].append({
        "type": 'pie',
        "id": 'pie',
        "radius": '30%',
        "center": ['50%', '25%'],
        "emphasis": {
        "focus": 'self'
        },
        "label": {
        "formatter": '{b}: {@' + baseline_list[0] + '} ({d}%)'
        },
        "encode": {
        "itemName": '对比项目',
        "value": baseline_list[0],
        "tooltip": baseline_list[0]
        }
    })
    return option

def add_compare_value(option, value_name, value_list, smooth=False):
    """
    增加一个对比目标，value_name是对比目标的名字，value_list是所有baseline在这个目标上的列表
    """
    data_list = [value_name]
    data_list.extend(value_list)
    assert len(data_list) == len(option["dataset"]["source"][0]), print("传入的数组长度和初始化的baseline数量不一致")
    option["dataset"]["source"].append(data_list)
    option["series"].append({ "type": 'line',
                         "smooth": smooth,
                        "seriesLayoutBy": 'row',
                        "emphasis": { "focus": 'series' } })


def plot_option(option, height=600):
    option["series"][0], option["series"][-1] = option["series"][-1], option["series"][0]
    option_json = json.dumps(option, ensure_ascii=False)
    opt = """
        <!DOCTYPE html>
            <html style="height: 100%">
            <head>
                <meta charset="utf-8">
                <title>ECharts</title>
                <!-- 引入 ECharts 文件 -->
                <script src="https://cdn.jsdelivr.net/npm/echarts@5.1.0/dist/echarts.min.js"></script>
            </head>
            <body style="height: 100%; margin: 0">
                <!-- 准备一个容器 -->
                <div id="main" style="height: 100%; width: 100%"></div>
                <script type="text/javascript">
                    var chartDom = document.getElementById('main');
                    var myChart = echarts.init(chartDom);
                    setTimeout(function () {
                        var option = {option_json};
                        myChart.on('updateAxisPointer', function (event) {
                        const xAxisInfo = event.axesInfo[0];
                        if (xAxisInfo) {
                        const dimension = xAxisInfo.value + 1;
                        myChart.setOption({
                            series: {
                            id: 'pie',
                            label: {
                                formatter: '{b}: {@[' + dimension + ']} ({d}%)'
                            },
                            encode: {
                                value: dimension,
                                tooltip: dimension
                            }
                            }
                        });
                        }
                    });
                    myChart.setOption(option);
                    });
            </script>
        </body>
        </html>
    """.replace("{option_json}", option_json)
    st.components.v1.html(opt, height=height)

if __name__ == "__main__":
    option = create_line_option(['2012', '2013', '2014', '2015', '2016', '2017'])
    add_compare_value(option, 'Matcha Latte', [ 56.5, 182.1, 88.7, 70.1, 53.4, 85.1])
    add_compare_value(option, 'Milk Tea', [51.1, 51.4, 55.1, 53.3, 73.8, 68.7])
    add_compare_value(option, 'Cheese Cocoa', [40.1, 62.2, 69.5, 36.4, 45.2, 32.5])
    add_compare_value(option, 'Walnut Brownie', [25.2, 37.1, 41.2, 18, 33.9, 49.1])

    plot_option(option)
