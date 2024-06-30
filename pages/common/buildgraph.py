import streamlit as st
from streamlit_echarts import st_echarts
import random
import copy

class GraphMeta:
    def __init__(self) -> None:
        self.maxvalue = 0
        self.meta_dict = {
            "nodes":[],
            "links":[]
        }
        self.tmpnodes = set()
        self.name_id = dict()
        
    def random_color(self):
        return "#{:06x}".format(random.randint(0, 0xFFFFFF))

    def add_node(self, name, value):
        node_set = self.tmpnodes
        if name not in node_set:
            self.meta_dict["nodes"].append({
                "id": len(node_set),
                "name": name,
                "value": value,
                "symbolSize": value,
                "label": {
                    "show": True
                },
                "itemStyle": {"color": self.random_color()}
            })
            self.name_id[name] = len(node_set)
            node_set.add(name)
            self.maxvalue = max(self.maxvalue, value)
    
    def get_value_by_name(self, name):
        assert name in self.tmpnodes, print(name, "不在图中")
        return self.meta_dict["nodes"][self.name_id[name]]["value"]

    def link_between(self, src, dst, w):
        if src not in self.tmpnodes:
            raise Exception(f"src【{src}】不在节点集合中，无法连接")
        if dst not in self.tmpnodes:
            raise Exception(f"dst【{dst}】不在节点集合中，无法连接")
        
        src_index = self.name_id[src]
        src_color = self.meta_dict["nodes"][src_index]["itemStyle"]["color"]
        self.meta_dict["links"].append({
            "source": src_index,
            "target": self.name_id[dst],
            "value": w,
            "lineStyle": {"color": src_color}
        })
    
    def clean_link(self):
        self.meta_dict["links"] = []
            
    
    def export_data(self):
        if self.maxvalue > 100:
            for node in self.meta_dict["nodes"]:
                node["symbolSize"] = node["symbolSize"] / self.maxvalue * 100
            self.maxvalue = 100
        return self.meta_dict

def plot_graph(graph, title, height=500):
    option = {
        "title": {
                "text": title,
                "subtext": "Force layout",
                "top": "bottom",
                "left": "right",
            },
        "tooltip": {},
        "animationDuration": 1500,
        "animationEasingUpdate": "quinticInOut",
        "series": [
            {
                "name": "zone_demand_mw",
                "type": "graph",
                "layout": "force",
                "data": graph["nodes"],
                "links": graph["links"],
                "roam": True,
                "label": {"position": "right", "formatter": "{b}"},
                "lineStyle": {"color": "source", "curveness": 0.5, "width": 2},
                "edgeSymbol": ["none", "arrow"],
                "emphasis": {"focus": "adjacency", "lineStyle": {"width": 10}},
                "force": {
                    "repulsion": 1000,
                    "edgeLength": [50, 200]
                }
            }
        ],
    }
    # 使用streamlit_echarts渲染图表
    st_echarts(option, height=height)

if __name__ == "__main__":
    graph_meta = GraphMeta()
    graph_meta.add_node("A", 20)
    graph_meta.add_node("B", 75)
    graph_meta.add_node("C", 15)
    graph_meta.add_node("D", 87)
    graph_meta.add_node("E", 100)
    graph_meta.link_between("A", "B", 10)
    graph_meta.link_between("A", "C", 100)
    graph_meta.link_between("C", "A", 78)
    graph_meta.link_between("B", "E", 21)
    graph = graph_meta.export_data()
    plot_graph(graph, "传输线路")
    
