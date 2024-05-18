# visualize_model.py
from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.ModularVisualization import ModularServer
from ethnocentrism_model import EthnocentrismModel
import param


# 定义代理的可视化呈现
def agent_portrayal(agent):
    portrayal = {"Shape": "rect",
                 "Filled": "false",
                 "Layer": 0,
                 "Color": agent.color,
                 "w": 0.8,
                 "h": 0.8,
                 "Text": agent.unique_id}

    # 为不同的代理特性设置不同的颜色和层级
    if agent.cooperate_with_same:
        portrayal["Shape"] = "circle"
        portrayal['r'] = 1
    else:
        portrayal["Shape"] = "rect"

    if agent.cooperate_with_different:
        portrayal["Filled"] = "true"
    else:
        portrayal["Filled"] = "false"
        portrayal["Color"] = "White"

    return portrayal


def run_server():
    grid = CanvasGrid(agent_portrayal, 50, 50, 500, 500)
    # 以下部分根据是否需要图表来决定是否加入
    # chart = ChartModule(...)

    model_params = {
        "n": 10,
        "width": 50,
        "height": 50
    }

    server = ModularServer(EthnocentrismModel,
                           [grid],  # 如果有图表，记得也添加 chart
                           "Ethnocentrism Model",
                           model_params)
    server.port = 8521  # 可以根据需要改变端口号
    server.launch()


if __name__ == '__main__':
    run_server()
