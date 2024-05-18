import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk

from matplotlib import collections
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.patches import Rectangle, Circle

import param
from ethnocentrism_agent import EthnocentrismAgent
from ethnocentrism_model import EthnocentrismModel



class ModelGUI(tk.Tk):
    def __init__(self, model):
        super().__init__()

        self.model = model

        # GUI settings
        self.cell_size = 11
        self.agent_size = 8
        self.canvas_size = self.model.grid.width * self.cell_size
        self.window_size = self.canvas_size
        self.running = False
        self.shapes = {}

        # Create the frames
        self.control_frame = tk.Frame(self, padx=10, pady=20)
        self.control_frame.grid(row=0, column=0, sticky="ns")

        self.canvas_frame = tk.Frame(self, padx=20, pady=20)
        self.canvas_frame.grid(row=0, column=1, rowspan=2, sticky="nsew")


        # Create the drawing canvas
        self.canvas = tk.Canvas(self.canvas_frame, width=self.canvas_size, height=self.canvas_size,
                                highlightbackground="black", highlightthickness=1)
        # Call it right after you create the canvas or whenever you need to redraw the grid:
        self.canvas.pack()

        # Control buttons
        tk.Button(self.control_frame, text="Start", command=self.start).pack(side="top")
        tk.Button(self.control_frame, text="Stop", command=self.stop).pack(side="top")
        tk.Button(self.control_frame, text="Step", command=self.step).pack(side="top")
        tk.Button(self.control_frame, text="Init Empty", command=self.init_empty).pack(side="top")
        tk.Button(self.control_frame, text="Init Full", command=self.init_full).pack(side="top")

        self.geometry(f"{self.window_size + 750}x{self.window_size + 80}")

        self.figure, self.ax = plt.subplots(figsize=(7, 4))
        plt.subplots_adjust(right=0.85)
        self.graph = FigureCanvasTkAgg(self.figure, master=self)  # 创建 figure 对象关联的 canvas 对象
        self.graph.get_tk_widget().grid(row=1, column=0)  # 将图形组件放在控制按钮下面 把 canvas 添加到 tkinter GUI 中


    def draw(self):
        gap = (self.cell_size - self.agent_size) / 2
        for agent in self.model.schedule.agents:
            x, y = agent.pos
            x = x * self.cell_size + gap
            y = y * self.cell_size + gap
            # Adjust y so the model is displayed in the typical grid orientation
            y = self.canvas_size - y - self.agent_size
            if agent.cooperate_with_same:
                if agent.cooperate_with_different:
                    self.shapes[agent.unique_id] = self.canvas.create_oval(
                        x, y, x + self.agent_size, y + self.agent_size,
                        fill=agent.color,
                        outline=agent.color)
                else:
                    self.shapes[agent.unique_id] = self.canvas.create_oval(
                        x, y, x + self.agent_size, y + self.agent_size,
                        fill="white",
                        outline=agent.color)
            else:
                if agent.cooperate_with_different:
                    self.shapes[agent.unique_id] = self.canvas.create_rectangle(
                        x, y, x + self.agent_size, y + self.agent_size,
                        fill=agent.color,
                        outline=agent.color)
                else:
                    self.shapes[agent.unique_id] = self.canvas.create_rectangle(
                        x, y, x + self.agent_size, y + self.agent_size,
                        fill="white",
                        outline=agent.color)

    def start(self):
        self.running = True
        self.run_model()

    def stop(self):
        self.running = False

    def step(self):
        self.model.step()
        self.canvas.delete('all')
        self.shapes = {}
        self.draw()
        self.update_graph()

    def run_model(self):
        while self.running:
            self.step()
            self.update()
        else:
            self.step()

    def init_empty(self):
        """清除所有代理并重置画布。"""
        self.model.schedule.agents.clear()  # 清除所有代理
        self.canvas.delete('all')  # 清除画布
        self.shapes = {}
        for agent_type in self.model.agent_count_dict.keys():
            self.model.agent_count_dict[agent_type] = [0 for i in range(self.model.schedule.steps)]

        self.update_graph()

    def init_full(self):
        """在每个格子中创建一个代理。"""
        self.canvas.delete('all')  # 清除画布
        self.shapes = {}
        for x in range(self.model.grid.width):
            for y in range(self.model.grid.height):
                color = self.model.random.choice(param.RANDOM_COLOR)  # 使用模型的随机数生成器
                cooperate_with_same = self.model.random.random() < param.IMMIGRANT_CHANCE_COOPERATE_WITH_SAME
                cooperate_with_different = self.model.random.random() < param.IMMIGRANT_CHANCE_COOPERATE_WITH_DIFFERENT
                agent = EthnocentrismAgent(self.model.next_id(), self.model, color,
                                           cooperate_with_same, cooperate_with_different)
                self.model.grid.place_agent(agent, (x, y))
                self.model.schedule.add(agent)

        self.draw()  # 重新绘制界面
        for agent_type in self.model.agent_count_dict.keys():
            self.model.agent_count_dict[agent_type] = [self.model.grid.width * self.model.grid.height for i in
                                                       range(self.model.schedule.steps)]
        self.update_graph()

    def update_graph(self):
        # 先清空一下原来的数据
        self.ax.cla()
        x = list(range(self.model.schedule.steps))  # x坐标
        for agent_type in self.model.agent_count_dict.keys():
            y = self.model.agent_count_dict[agent_type]
            self.ax.plot(x, y, label=agent_type)  # 画一条线
        self.ax.legend()  # 添加图例
        self.ax.set_title("Strategy Counts")  # 在这里添加标题
        self.ax.set_xlabel("Time")  # 设置x轴的标题
        self.ax.set_ylabel("Count")  # 设置y轴的标题

        # 把图例放在右侧并且确保图例不和图形相交
        self.ax.legend(loc="center left", bbox_to_anchor=(1, 0.5))
        self.graph.draw()  # 更新图形


if __name__ == "__main__":
    model = EthnocentrismModel(n=10, width=50, height=50)
    app = ModelGUI(model)
    app.mainloop()