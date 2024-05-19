from mesa import Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation

import param
from ethnocentrism_agent import EthnocentrismAgent


class EthnocentrismModel(Model):
    def __init__(self, n, width, height):
        super().__init__()
        self.num_agents = n
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)
        for _ in range(self.num_agents):
            # 在一个随机但空的单元格中创建代理
            self.create_agent()
        self.agent_count_dict = {'CC': [],  # same_true_diff_true
                                 'CD': [],  # same_true_diff_false
                                 'DC': [],  # same_false_diff_true
                                 'DD': []}  # same_false_diff_false

    def step(self):
        for _ in range(
                min(param.IMMIGRANTS_PER_DAY, self.grid.width * self.grid.height - self.schedule.get_agent_count())):
            self.create_agent()
        self.schedule.step()
        self.death()
        for agent_type in self.agent_count_dict.keys():
            # Map agent_type to corresponding cooperate_with_same and cooperate_with_different values
            same = True if agent_type[0] == 'C' else False
            diff = True if agent_type[1] == 'D' else False
            self.agent_count_dict[agent_type].append(
                sum([1 for a in self.schedule.agents if
                     a.cooperate_with_same == same and a.cooperate_with_different == diff])
            )

    def create_agent(self):
        # 首先找到所有空的单元格
        empty_cells = [(x, y) for (x, y) in self.grid.empties]
        if not empty_cells:  # 若没有空单元格，则无法创建新代理
            return
        # 从空单元格列表中随机选择一个位置
        x, y = self.random.choice(empty_cells)
        color = self.random.choice(param.RANDOM_COLOR)
        cooperate_with_same = self.random.random() < param.IMMIGRANT_CHANCE_COOPERATE_WITH_SAME
        cooperate_with_different = self.random.random() < param.IMMIGRANT_CHANCE_COOPERATE_WITH_DIFFERENT
        # 创建一个新代理，并将其添加到网格和调度器中
        agent = EthnocentrismAgent(self.next_id(), self, color, cooperate_with_same, cooperate_with_different)
        self.grid.place_agent(agent, (x, y))
        self.schedule.add(agent)

    def death(self):
        # Shuffle agents before determining death to avoid bias
        all_agents = list(self.schedule.agents)  # Get a list of all agents
        self.random.shuffle(all_agents)  # Shuffle the list
        for agent in all_agents:  # Iterate through the shuffled list
            if self.random.random() < param.DEATH_RATE:
                self.grid.remove_agent(agent)
                self.schedule.remove(agent)

