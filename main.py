import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk

from matplotlib import collections
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.patches import Rectangle, Circle

import param
from ethnocentrism_agent import EthnocentrismAgent
from ethnocentrism_model import EthnocentrismModel
from param import RANDOM_COLOR


class ModelGUI(tk.Tk):
    def __init__(self, model):
        super().__init__()

        self.model = model

        # GUI settings
        self.cell_size = 10
        self.canvas_size = self.model.grid.width * self.cell_size
        self.running = False
        self.shapes = {}

        # Create the frames
        self.control_frame = tk.Frame(self)
        self.control_frame.grid(row=0, column=0, sticky="ns")

        self.canvas_frame = tk.Frame(self)
        self.canvas_frame.grid(row=0, column=1, sticky="nsew")

        # Create the drawing canvas
        self.canvas = tk.Canvas(self.canvas_frame, width=self.canvas_size, height=self.canvas_size,
                                highlightbackground="black", highlightthickness=1)
        # Call it right after you create the canvas or whenever you need to redraw the grid:
        self.canvas.pack()

        # Control buttons
        tk.Button(self.control_frame, text="Start", command=self.start).pack(side="top")
        tk.Button(self.control_frame, text="Stop", command=self.stop).pack(side="top")
        tk.Button(self.control_frame, text="Step", command=self.step).pack(side="top")
        tk.Button(self.control_frame, text="Reset", command=self.reset).pack(side="top")
        tk.Button(self.control_frame, text="Init Empty", command=self.init_empty).pack(side="top")
        tk.Button(self.control_frame, text="Init Full", command=self.init_full).pack(side="top")

    # def draw(self):
    #     fig, ax = plt.subplots(figsize=(5, 5))
    #
    #     agents = self.model.schedule.agents
    #     shapes = []
    #     facecolors = []  # Fill colors
    #     edgecolors = []  # Edge colors
    #
    #     for agent in agents:
    #         x, y = agent.pos
    #
    #         if agent.cooperate_with_same:
    #             shape = Circle((x + 0.5, self.model.grid.height - y - 0.5), radius=0.4)
    #         else:
    #             shape = Rectangle((x + 0.1, self.model.grid.height - y - 0.9), 0.8, 0.8)
    #
    #         shapes.append(shape)
    #         edgecolors.append(agent.color)
    #
    #         if agent.cooperate_with_different:
    #             facecolors.append(agent.color)
    #         else:
    #             facecolors.append("none")
    #
    #     collection = collections.PatchCollection(shapes, facecolors=facecolors, edgecolors=edgecolors)
    #     ax.add_collection(collection)
    #
    #     ax.set_xlim(0, self.model.grid.width)
    #     ax.set_ylim(0, self.model.grid.height)
    #
    #     # Set the locations of the grid lines
    #     ax.set_xticks(np.arange(0, self.model.grid.width, 1))
    #     ax.set_yticks(np.arange(0, self.model.grid.height, 1))
    #
    #     # Show the grid
    #     ax.grid(True)
    #
    #     # This line is needed to align the plotting of data and the grid
    #     ax.set_axisbelow(True)
    #
    #     if self.canvas is not None:
    #         self.canvas.get_tk_widget().pack_forget()
    #
    #     self.canvas = FigureCanvasTkAgg(fig, master=self)
    #     self.canvas.draw()
    #     self.canvas.get_tk_widget().pack(side="top", fill="both", expand=1)
    #     plt.close(fig)

    def draw(self):
        for agent in self.model.schedule.agents:
            x, y = agent.pos
            x *= self.cell_size
            y *= self.cell_size
            # Adjust y so the model is displayed in the typical grid orientation
            y = int(self.canvas['height']) - y
            if agent.cooperate_with_same:
                if agent.cooperate_with_different:
                    self.shapes[agent.unique_id] = self.canvas.create_oval(
                        x, y, x + self.cell_size, y + self.cell_size,
                        fill=agent.color,
                        outline=agent.color)
                else:
                    self.shapes[agent.unique_id] = self.canvas.create_oval(
                        x, y, x + self.cell_size, y + self.cell_size,
                        fill="white",
                        outline=agent.color)
            else:
                if agent.cooperate_with_different:
                    self.shapes[agent.unique_id] = self.canvas.create_rectangle(
                        x, y, x + self.cell_size, y + self.cell_size,
                        fill=agent.color,
                        outline=agent.color)
                else:
                    self.shapes[agent.unique_id] = self.canvas.create_rectangle(
                        x, y, x + self.cell_size, y + self.cell_size,
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

    def reset(self):
        self.model = EthnocentrismModel(n=10, width=50, height=50)
        self.canvas.delete('all')
        self.shapes = {}
        self.draw()
        self.stop()

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


if __name__ == "__main__":
    model = EthnocentrismModel(n=10, width=50, height=50)
    app = ModelGUI(model)
    app.mainloop()