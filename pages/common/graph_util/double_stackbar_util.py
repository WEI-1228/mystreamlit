import streamlit as st
import json

class CompareTwoStackBar:
    def __init__(self, baseline_name_list) -> None:
        """
        初始必须确定baseline的数量，而一条柱分成多少比例，是动态添加的
        """
        self.ylabel = baseline_name_list
        self.baseline_num = len(baseline_name_list)
        self.data1 = []
        self.data2 = []
        self.part1_name_list = []
        self.part2_name_list = []
    
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
    
    def add_left_part(self, partname, left_baseline_list):
        """
        为每个baseline增加一部分数据，相当于增加一条柱的一部分比例，必须传入这部分比例的名称
        """
        if len(left_baseline_list) != self.baseline_num:
            raise Exception("左半部分长度错误")
            
        self.data1.append(left_baseline_list)
        self.part1_name_list.append(partname)
    
    def add_right_part(self, partname, right_baseline_list):
        """
        为每个baseline增加一部分数据，相当于增加一条柱的一部分比例，必须传入这部分比例的名称
        """
        if len(right_baseline_list) != self.baseline_num:
            raise Exception("右半部分长度错误")
            
        self.data2.append(right_baseline_list)
        self.part2_name_list.append(partname)
    
    def export_html(self):
        data1 = self.calculate_percent(self.data1)
        data2 = self.calculate_percent(self.data2)
        self.series_list = []
        for d, n in zip(data1, self.part1_name_list):
            self.append_series(self.series_list, n, d, 0)
        
        for d, n in zip(data2, self.part2_name_list):
            self.append_series(self.series_list, n, d, 1)
        
        return self.convert(self.ylabel, self.series_list, data1, data2)
        
    
    def append_series(self, series_list, name, baseline_list, graph_id):
        series = {
            "name": name,
            "type": 'bar',
            "stack": "stack" + str(graph_id),
            "label": {"show": "true", "formatter": '{c}%'},
            "emphasis": {"focus": 'series'},
            "data": baseline_list,
            "xAxisIndex": graph_id,
            "yAxisIndex": graph_id
        }
        series_list.append(series)
    
    def convert(self, ylabal, series, data1, data2):
        ylabel_json = self.to_json(ylabal)
        series_json = self.to_json(series)
        data1_json = self.to_json(data1)
        data2_json = self.to_json(data2)
        html = """
            <!DOCTYPE html>
            <html style="height: 100%">
            <head>
                <meta charset="utf-8">
                <title>ECharts</title>
                <!-- 引入 ECharts 文件 -->
                <script src="https://cdn.jsdelivr.net/npm/echarts@5.0.0/dist/echarts.min.js"></script>
            </head>
            <body style="height: 100%; margin: 0">
                <!-- 准备一个容器 -->
                <div id="main" style="height: 100%; width: 100%"></div>
                <script type="text/javascript">
                    var chartDom = document.getElementById('main');
                    var myChart = echarts.init(chartDom);
                    var option;

                    var data1Percent = ${data1};
                    var data2Percent = ${data2};

                    option = {
                        tooltip: {
                            trigger: 'axis',
                            axisPointer: {
                                type: 'shadow'
                            },
                            formatter: function (params) {
                                let result = params[0].name + '<br/>';
                                params.forEach(function (item) {
                                    result += item.marker + " " + item.seriesName + ": " + item.data + '%<br/>';
                                });
                                return result;
                            }
                        },
                        legend: {},
                        grid: [
                            {left: '3%', right: '53%', bottom: '3%', containLabel: true},
                            {left: '53%', right: '3%', bottom: '3%', containLabel: true}
                        ],
                        xAxis: [
                            {type: 'value', gridIndex: 0, max: 100},
                            {type: 'value', gridIndex: 1, max: 100}
                        ],
                        yAxis: [
                            {type: 'category', data: ${ylabel}, gridIndex: 0},
                            {type: 'category', data: ${ylabel}, gridIndex: 1}
                        ],
                        series: ${series}
                    };

                    myChart.setOption(option);
                </script>
            </body>
            </html>
            """
        return html.replace("${ylabel}",ylabel_json).replace("${data1}", data1_json).replace("${data2}", data2_json).replace("${series}", series_json)

    def export_df(self):
        return self.data1, self.data2
    
if __name__ == "__main__":
    stack = CompareTwoStackBar(['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'])
    stack.add_left_part("a", [320, 302, 301, 334, 390, 330, 320])
    stack.add_left_part("b", [320, 302, 301, 334, 390, 330, 320])
    stack.add_left_part("c", [320, 302, 301, 334, 390, 330, 320])
    stack.add_right_part("d", [320, 302, 301, 334, 390, 330, 320])
    stack.add_right_part("e", [320, 302, 301, 334, 390, 330, 320])
    stack.add_right_part("f", [320, 302, 301, 334, 390, 330, 320])
    stack.add_right_part("g", [320, 302, 301, 334, 390, 330, 320])

    ht = stack.export_html()
    st.text(ht)
    st.components.v1.html(ht, height=500)


