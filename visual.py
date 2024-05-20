import random

import tkinter as tk


import param

from agent import EthnocentrismAgent
from model import EthnocentrismModel


class ModelGUI(tk.Tk):
    def __init__(self, model):
        super().__init__()

        self.model = model

        # GUI settings
        self.cell_size = 11
        self.agent_size = 8
        self.canvas_size = self.model.grid_width * self.cell_size
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


    def draw(self):
        gap = (self.cell_size - self.agent_size) / 2
        for agent in self.model.schedule:
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
    #     self.draw()


    # def run_model(self):
    #     while self.running:
    #         self.step()
    #         self.update()
    #     else:
    #         self.step()

    def run_model(self):
        steps = 0  # 初始化步数计数器
        while self.running and steps < 1000:  # 运行一千步后停止
            self.step()
            self.update()
            steps += 1
        self.running = False  # 运行结束后确保模型停止

    def init_empty(self):
        """清除所有代理并重置画布。"""
        self.model.schedule.clear()  # 直接清除 schedule 列表中的所有代理
        self.canvas.delete('all')  # 清除画布
        self.shapes = {}
        # Additionally, you will likely want to reset the grid as well.
        self.model.grid = {(x, y): None for x in range(self.model.grid_width) for y in range(self.model.grid_height)}

    def init_full(self):
        """Create an agent in every cell."""
        self.canvas.delete('all')  # Clear the canvas
        self.shapes = {}
        self.model.grid = {(x, y): None for x in range(self.model.grid_width) for y in range(self.model.grid_height)}
        self.model.schedule = []
        for x in range(self.model.grid_width):
            for y in range(self.model.grid_height):
                unique_id = len(self.model.schedule)
                color = random.choice(param.RANDOM_COLOR)
                cooperate_with_same = random.random() < param.IMMIGRANT_CHANCE_COOPERATE_WITH_SAME
                cooperate_with_different = random.random() < param.IMMIGRANT_CHANCE_COOPERATE_WITH_DIFFERENT
                pos = (x, y)  # Define the position tuple
                agent = EthnocentrismAgent(unique_id, self.model, color,
                                           cooperate_with_same, cooperate_with_different, pos)
                self.model.grid[pos] = agent
                self.model.schedule.append(agent)

        self.draw()  # Redraw the interface



if __name__ == "__main__":
    model = EthnocentrismModel(n=10, width=50, height=50)
    app = ModelGUI(model)
    app.mainloop()