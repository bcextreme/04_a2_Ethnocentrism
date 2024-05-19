import csv
import random

import param
from agent import EthnocentrismAgent


class EthnocentrismModel:
    def __init__(self, n, width, height):
        self.num_agents = n
        self.grid_width = width
        self.grid_height = height
        self.schedule = []
        self.grid = {(x, y): None for x in range(width) for y in range(height)}
        self.current_id = 0
        self.step_count = 0
        for i in range(self.num_agents):
            self.create_agent()

        self.agent_count_dict = {'CC': [],  # same_true_diff_true
                                 'CD': [],  # same_true_diff_false
                                 'DC': [],  # same_false_diff_true
                                 'DD': []}  # same_false_diff_false

        self.csv_file = open('model_output.csv', mode='w', newline='', encoding='utf-8')
        self.csv_writer = csv.writer(self.csv_file)
        self.csv_writer.writerow(
            ["UniqueID", "PosX", "PosY", "Color", "CooperateWithSame", "CooperateWithDifferent", "Step"])



    def step(self):
        self.record_agents_state()
        self.step_count += 1
        empty_cells = len([pos for pos, agent in self.grid.items() if agent is None])

        num_new_agents = min(param.IMMIGRANTS_PER_DAY, empty_cells)
        for _ in range(num_new_agents):
            self.create_agent()  # Assign a new unique ID based on the current schedule size

        # Simulation step for each agent
        random.shuffle(self.schedule)
        for agent in self.schedule:
            # Assume each agent has a step method to define its actions
            agent.step()
        self.death()
        for agent_type in self.agent_count_dict.keys():
            # Map agent_type to corresponding cooperate_with_same and cooperate_with_different values
            same = agent_type[0] == 'C'
            diff = agent_type[1] == 'C'

            self.agent_count_dict[agent_type].append(
                sum(1 for agent in self.schedule if
                    agent.cooperate_with_same == same and agent.cooperate_with_different == diff)
            )

    def create_agent(self):
        empty_cells = [k for k, v in self.grid.items() if v is None]
        if not empty_cells:
            return

        pos = random.choice(empty_cells)
        color = random.choice(param.RANDOM_COLOR)
        cooperate_with_same = random.random() < param.IMMIGRANT_CHANCE_COOPERATE_WITH_SAME
        cooperate_with_different = random.random() < param.IMMIGRANT_CHANCE_COOPERATE_WITH_DIFFERENT

        # 注意这里我们也传递了位置 pos 给代理
        agent = EthnocentrismAgent(
            unique_id=self.next_id(),
            model=self,
            color=color,
            cooperate_with_same=cooperate_with_same,
            cooperate_with_different=cooperate_with_different,
            pos=pos  # 这里传递了pos
        )

        self.grid[pos] = agent
        self.schedule.append(agent)

    def get_neighbors(self, pos, moore=False, all=False):
        directions = [
            (-1, 0),  # Left
            (1, 0),  # Right
            (0, -1),  # Down
            (0, 1),  # Up
        ]

        if moore:
            # Include diagonal neighbors
            directions += [
                (-1, -1),  # Bottom Left
                (-1, 1),  # Top Left
                (1, -1),  # Bottom Right
                (1, 1),  # Top Right
            ]

        neighbors = []
        for dx, dy in directions:
            x, y = pos[0] + dx, pos[1] + dy

            # Check if (x, y) is within the bounds of the grid
            if 0 <= x < self.grid_width and 0 <= y < self.grid_height:
                if all:  # Return all positions
                    neighbors.append((x, y))
                else:  # Return positions only if they are occupied
                    if self.grid.get((x, y)) is not None:
                        neighbors.append((x, y))

        return neighbors

    def death(self):
        random.shuffle(self.schedule)  # Now we shuffle the list
        alive_agents = []
        for agent in self.schedule:
            if random.random() >= param.DEATH_RATE:
                alive_agents.append(agent)
            else:
                # Mark the agent's cell as empty
                self.grid[agent.pos] = None  # Assuming each agent knows its position
        self.schedule = alive_agents

    def next_id(self):
        # 返回当前的ID，并将其递增以供下次使用
        self.current_id += 1
        return self.current_id - 1

    def record_agents_state(self):
        for agent in self.schedule:
            self.csv_writer.writerow([
                agent.unique_id,
                agent.pos[0],  # PosX
                agent.pos[1],  # PosY
                agent.color,
                agent.cooperate_with_same,
                agent.cooperate_with_different,
                self.step_count
            ])

    def __del__(self):  # 模型被销毁时触发
        self.csv_file.close()  # 确保文件被正确关闭
