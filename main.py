import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk

from matplotlib import collections
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.patches import Rectangle, Circle
from ethnocentrism_model import EthnocentrismModel

class ModelGUI(tk.Tk):
    def __init__(self, model):
        super().__init__()

        self.geometry("800x600")
        self.model = model
        self.canvas = None

        self.running = False
        self.model_reset = False

        self.step_button = tk.Button(self, text="Step", command=self.step)
        self.step_button.pack(side="top")

        self.start_button = tk.Button(self, text="Start", command=self.start)
        self.start_button.pack(side="top")

        self.stop_button = tk.Button(self, text="Stop", command=self.stop)
        self.stop_button.pack(side="top")

        self.reset_button = tk.Button(self, text="Reset", command=self.reset)
        self.reset_button.pack(side="top")

    def draw(self):
        fig, ax = plt.subplots(figsize=(5, 5))

        agents = self.model.schedule.agents
        shapes = []
        facecolors = []  # Fill colors
        edgecolors = []  # Edge colors

        for agent in agents:
            x, y = agent.pos

            if agent.cooperate_with_same:
                shape = Circle((x + 0.5, self.model.grid.height - y - 0.5), radius=0.4)
            else:
                shape = Rectangle((x + 0.1, self.model.grid.height - y - 0.9), 0.8, 0.8)

            shapes.append(shape)
            edgecolors.append(agent.color)

            if agent.cooperate_with_different:
                facecolors.append(agent.color)
            else:
                facecolors.append("none")

        collection = collections.PatchCollection(shapes, facecolors=facecolors, edgecolors=edgecolors)
        ax.add_collection(collection)

        ax.set_xlim(0, self.model.grid.width)
        ax.set_ylim(0, self.model.grid.height)

        # Set the locations of the grid lines
        ax.set_xticks(np.arange(0, self.model.grid.width, 1))
        ax.set_yticks(np.arange(0, self.model.grid.height, 1))

        # Show the grid
        ax.grid(True)

        # This line is needed to align the plotting of data and the grid
        ax.set_axisbelow(True)

        if self.canvas is not None:
            self.canvas.get_tk_widget().pack_forget()

        self.canvas = FigureCanvasTkAgg(fig, master=self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side="top", fill="both", expand=1)
        plt.close(fig)

    def step(self):
        self.model.step()
        self.draw()

    def start(self):
        self.running = True
        self.run_model()

    def stop(self):
        self.running = False

    def reset(self):
        self.running = False
        self.model_reset = True
        self.model = EthnocentrismModel(n=10, width=50, height=50)  # Reset the model
        self.draw()

    def run_model(self):
        while self.running and not self.model_reset:
            self.model.step()

        self.model_reset = False

if __name__ == "__main__":
    model = EthnocentrismModel(n=10, width=50, height=50)
    app = ModelGUI(model)
    app.mainloop()