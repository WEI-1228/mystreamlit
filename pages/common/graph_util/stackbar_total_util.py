import streamlit as st
import json

class CompareTwoStackBar:
    def __init__(self, baseline_name_list) -> None:
        """
        初始必须确定baseline的数量，而一条柱分成多少比例，是动态添加的
        """
        self.ylabel = baseline_name_list
        self.baseline_num = len(baseline_name_list)
        self.data = []
        self.part_name_list = []
    
    def to_json(self, object):
        return json.dumps(object)

    def calculate_percent(self, data):
        result = []
        for series in data:
            series_percent = []
            for index, value in enumerate(series):
                total = sum(series[index] for series in data)
                percent = (value / total * 100) if total != 0 else 0
                series_percent.append(round(percent, 2))
            result.append(series_percent)
        return result
    
    def add_part(self, partname, baseline_list):
        """
        为每个baseline增加一部分数据，相当于增加一条柱的一部分比例，必须传入这部分比例的名称
        """
        if len(baseline_list) != self.baseline_num:
            raise Exception("左半部分长度错误")
            
        self.data.append(baseline_list)
        self.part_name_list.append(partname)
    
    def export_html(self):
        data = self.data.copy()
        self.series_list = []
        for d, n in zip(data, self.part_name_list):
            self.append_series(self.series_list, n, d)
        return self.convert(self.ylabel, self.series_list, self.data)
        
    
    def append_series(self, series_list, name, baseline_list):
        series = {
            "name": name,
            "type": 'bar',
            "stack": 'total',
            # "label": {"show": "true", "formatter": '{c}%', "rotate": 90},
            "label": {"show": True},
            "emphasis": {"focus": 'series'},
            "data": baseline_list,
        }
        series_list.append(series)
    
    def convert(self, ylabal, series, data):
        ylabel_json = self.to_json(ylabal)
        series_json = self.to_json(series)
        data_json = self.to_json(data)
        html = """
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
                    option = {
                        tooltip: {
                            trigger: 'axis',
                            axisPointer: {
                            // Use axis to trigger tooltip
                            type: 'shadow' // 'shadow' as default; can also be 'line' or 'shadow'
                            }
                        },
                        legend: {},
                        toolbox: {
                feature: {
                    saveAsImage: {
                        type: 'png', // 保存为 SVG 格式
                        pixelRatio: 2
                    }
                }
            },
                        grid: {
                            left: '3%',
                            right: '4%',
                            bottom: '3%',
                            top: '10%',
                            containLabel: true
                        },
                        yAxis: {
                            type: 'value'
                        },
                        xAxis: {
                            type: 'category',
                            data: ${ylabel}
                        },
                        series: ${series}
                        };
                        toolbox: {
                    feature: {
                        saveAsImage: {
                            title: '保存图片'
                        }
                    }
                }
                    option.series.forEach(function (series) {
                                series.label = {
                                    show: true,
                                    formatter: function (params) {
                                        return params.value === 0 ? '' : params.value;
                                    },
                                };
                                //series.barWidth = '80'; // 设置柱子的宽度
                                series.emphasis = {
                                    focus: "series"
                                };
                            });
                    
                    // Assuming `option` is already defined as per your configuration.

        // Assuming `option` is already defined as per your configuration.

// Calculate sums for each data point
var sumData = Array(option.xAxis.data.length).fill(0);
option.series.forEach(function(series) {
    series.data.forEach(function(value, index) {
        sumData[index] += value;
    });
});

// Apply smaller markPoints to one of the existing series to display sums at the top
option.series.forEach(function(series, index) {
    series.markPoint = {
        data: sumData.map((sum, i) => ({
            coord: [i, sum], // Position at the top of each stack
            value: sum, // The sum value
            symbolSize: 30, // Smaller symbol size
            itemStyle: {
                color: 'red' // Mark points in red color
            }
        })),
        label: {
            show: true,
            position: 'top', // Labels are displayed on top of the mark points
            formatter: function(params) {
                return params.value; // Show the sum value as label
            }
        }
    };
});

// Assuming `myChart' is the instance of your echarts
myChart.setOption(option);
                    
                </script>
            </body>
            </html>
            """
        return html.replace("${ylabel}",ylabel_json).replace("${data}", data_json).replace("${series}", series_json)

    def export_df(self):
        return self.data
    
if __name__ == "__main__":
    stack = CompareTwoStackBar(['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'])
    stack.add_part("a", [320, 302, 301, 334, 390, 330, 320])
    stack.add_part("b", [320, 302, 301, 334, 390, 330, 320])
    stack.add_part("c", [320, 302, 301, 334, 390, 330, 320])

    ht = stack.export_html()
    # st.text(ht)
    st.components.v1.html(ht, height=500)


