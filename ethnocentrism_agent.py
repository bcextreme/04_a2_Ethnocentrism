from mesa import Agent

import param


class EthnocentrismAgent(Agent):
    def __init__(self, unique_id, model, color, cooperate_with_same, cooperate_with_different):
        super().__init__(unique_id, model)
        self.color = color
        self.cooperate_with_same = cooperate_with_same
        self.cooperate_with_different = cooperate_with_different
        self.ptr = param.INITIAL_PTR

    def step(self):
        self.interact()
        self.reproduce()

    def interact(self):
        neighbors = self.model.grid.get_neighbors(self.pos, moore=False)
        for other_agent in neighbors:
            if self.color == other_agent.color:
                if self.cooperate_with_same:
                    if self.ptr - param.COST_OF_GIVING >= 0:
                        self.ptr -= param.COST_OF_GIVING
                        other_agent.ptr += param.GAIN_OF_RECEIVING
            else:
                if self.ptr - param.COST_OF_GIVING >= 0:
                    if self.cooperate_with_different:
                        self.ptr -= param.COST_OF_GIVING
                        other_agent.ptr += param.GAIN_OF_RECEIVING

    def reproduce(self):
        # 用该代理的生殖潜能(ptr)作为生殖的概率
        if self.model.random.random() < self.ptr:
            # 找一个空位以放置新的代理
            empty_cells = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False, radius=1)
            empty_cells = [cell for cell in empty_cells if self.model.grid.is_cell_empty(cell)]
            if empty_cells:  # 如果有空位
                new_pos = self.model.random.choice(empty_cells)
                # 创建代理，考虑突变
                new_agent = EthnocentrismAgent(
                    self.model.next_id(),
                    self.model,
                    self.mutate_color(self.color),  # 可能发生突变的颜色
                    self.mutate_strategy(self.cooperate_with_same),  # 可能发生突变的合作策略
                    self.mutate_strategy(self.cooperate_with_different)  # 可能发生突变的合作策略
                )
                self.model.grid.place_agent(new_agent, new_pos)
                self.model.schedule.add(new_agent)

    def mutate_color(self, color):
        # 简单示例：有小概率改变颜色
        if self.model.random.random() < param.MUTATION_RATE:  # 突变率
            return self.model.random.choice(param.RANDOM_COLOR)
        else:
            return color

    def mutate_strategy(self, strategy):
        # 简单示例：有小概率改变策略
        if self.model.random.random() < param.MUTATION_RATE:  # 突变率
            return not strategy
        else:
            return strategy
