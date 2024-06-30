import streamlit as st
from streamlit_echarts import st_echarts
import json

option = {
  "legend": {},
  "tooltip": {
            "trigger": 'axis',
            "axisPointer": {
            "type": 'cross'
            }
        },
  "dataset": {
    "source": [
        
      ['product', '2015', '2016', '2017'], # baseline的数量 一组放一起对比的数据中的标签，比如v1,v2,v3，有多少个对比的baseline就有多少个数据
      ['Matcha Latte', 43.3, 85.8, 93.7], # 每一行都是一种需要对比的结果，需要对比多少个结果，就得有多少行，每行里面就放各个baseline的结果
      ['Milk Tea', 83.1, 73.4, 55.1],
      ['Cheese Cocoa', 86.4, 65.2, 82.5],
      ['Walnut Brownie', 72.4, 53.9, 39.1]
    ]
  },
  "xAxis": { "type": 'category' },
  "yAxis": {
    "axisLabel": {
      "formatter": "km"
    }
  },
  "series": [{ "type": 'bar' }, { "type": 'bar' }, { "type": 'bar' }] # 有多少组baseline就要放多少个
}

def create_bar_option(baseline_num, baseline_list):
    """
    需要对比的baseline的数量，以及每个baseline的名称列表
    """
    baseline_list = ["对比项目"] + baseline_list
    option = {
        "legend": {},
        "tooltip": {
                    "trigger": 'axis',
                    "axisPointer": {
                    "type": 'cross'
                    }
                },
        "dataset": {
            "source": [
                baseline_list, 
            ]
        },
        "xAxis": { "type": 'category' },
        "yAxis": {
            "axisLabel": {
                "formatter": "{value}"
            }
        },
        "series": [{ "type": 'bar' }, { "type": 'bar' }, { "type": 'bar' }] # 有多少组baseline就要放多少个
    }
    # option["series"] = [{ "type": 'bar' }] * baseline_num
    option["series"] = [{ "type": 'bar', "label": {"show": "true", "position": "top"} }] * baseline_num
        
    return option

def add_compare_value(option, value_name, value_list):
    """
    增加一个对比目标，value_name是对比目标的名字，value_list是所有baseline在这个目标上的列表
    """
    data_list = [value_name]
    data_list.extend(value_list)
    assert len(data_list) == len(option["dataset"]["source"][0]), print("传入的数组长度和初始化的baseline数量不一致")
    option["dataset"]["source"].append(data_list)

def plot_option(option, height=400, danwei=None, bignum=False):
    option_json = json.dumps(option, ensure_ascii=False)
    if bignum:
        if danwei:
            option_json = option_json.replace('"{value}"', 'function (value) {return value.toExponential(2) + "kw";}')
        else:
            option_json = option_json.replace('"{value}"', 'function (value) {return value.toExponential(2);}')
    else:
        if danwei:
            option_json = option_json.replace('"{value}"', '"{value} ' + danwei + '"')
            
    st.components.v1.html(f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <script src="https://cdn.jsdelivr.net/npm/echarts@latest/dist/echarts.min.js"></script>
    </head>
    <body>
        <div id="main" style="height: {height}px;"></div>
        <script type="text/javascript">
            // 基于准备好的dom，初始化echarts实例
            var myChart = echarts.init(document.getElementById('main'));
            // 指定图表的配置项和数据
            var option = {option_json};
            // 使用刚指定的配置项和数据显示图表
            myChart.setOption(option);
        </script>
    </body>
    </html>
    """, height=height)

if __name__ == "__main__":
    option = create_bar_option(3, ['2015', '2016', '2017'])
    add_compare_value(option, 'Matcha Latte', [43.3, 85.8, 93.7])
    add_compare_value(option, 'Milk Tea', [83.1, 73.4, 55.1])
    add_compare_value(option, 'Cheese Cocoa', [86.4, 65.2, 82.5])
    plot_option(option)
