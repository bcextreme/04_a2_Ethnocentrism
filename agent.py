import param
import random


class EthnocentrismAgent:

    def __init__(self, unique_id, model, color, cooperate_with_same, cooperate_with_different, pos):
        self.unique_id = unique_id
        self.model = model
        self.color = color
        self.cooperate_with_same = cooperate_with_same
        self.cooperate_with_different = cooperate_with_different
        self.ptr = param.INITIAL_PTR
        self.pos = pos  # 保存代理的位置

    def step(self):
        self.interact()
        self.reproduce()

    def interact(self):
        neighbors_coords = self.model.get_neighbors(self.pos, moore=False, all=False)  # 只获取存在的
        neighbors = [self.model.grid.get(pos) for pos in neighbors_coords]  # 获取agent对象
        for other_agent in neighbors:
            if self.color == other_agent.color:
                if self.cooperate_with_same and other_agent.cooperate_with_same:
                    if (self.ptr - param.COST_OF_GIVING >= 0) and (other_agent.ptr - param.COST_OF_GIVING >= 0):
                        self.ptr -= param.COST_OF_GIVING
                        other_agent.ptr += param.GAIN_OF_RECEIVING
            else:
                if (self.ptr - param.COST_OF_GIVING >= 0) and (other_agent.ptr - param.COST_OF_GIVING >= 0):
                    if self.cooperate_with_different and other_agent.cooperate_with_different:
                        self.ptr -= param.COST_OF_GIVING
                        other_agent.ptr += param.GAIN_OF_RECEIVING

    def reproduce(self):
        # 使用该代理的生殖潜能(ptr)作为生殖的概率
        if random.random() < self.ptr:
            # 获取周围的Agent对象
            neighbor_all_coords = set(self.model.get_neighbors(self.pos, moore=False, all=True))
            neighbor_coords = set(self.model.get_neighbors(self.pos, moore=False, all=False))
            # 获取周围的空格子坐标
            empty_cells = list(neighbor_all_coords - neighbor_coords)
            if empty_cells:  # 如果有空位
                new_pos = random.choice(empty_cells)
                # 创建代理，考虑突变
                new_agent = EthnocentrismAgent(
                    unique_id=self.model.next_id(),
                    model=self.model,
                    color=self.mutate_color(self.color),  # 可能发生突变的颜色
                    cooperate_with_same=self.mutate_strategy(self.cooperate_with_same),  # 可能发生突变的合作策略
                    cooperate_with_different=self.mutate_strategy(self.cooperate_with_different),  # 可能发生突变的合作策略
                    pos=new_pos  # 新代理的位置
                )

                self.model.grid[new_pos] = new_agent
                self.model.schedule.append(new_agent)

    def mutate_color(self, color):
        # 简单示例：有小概率改变颜色
        if random.random() < param.MUTATION_RATE:  # 突变率
            return random.choice(param.RANDOM_COLOR)
        else:
            return color

    def mutate_strategy(self, strategy):
        # 简单示例：有小概率改变策略
        if random.random() < param.MUTATION_RATE:  # 突变率
            return not strategy
        else:
            return strategy
