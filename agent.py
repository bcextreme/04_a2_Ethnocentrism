import param
import random


class EthnocentrismAgent:
    # Initializes an agent.
    def __init__(self, unique_id, model, color, 
                 cooperate_with_same, cooperate_with_different, pos):
        self.unique_id = unique_id
        self.model = model
        self.color = color
        self.cooperate_with_same = cooperate_with_same
        self.cooperate_with_different = cooperate_with_different
        self.ptr = param.INITIAL_PTR
        self.pos = pos  # Save the agent's position

    # Performs a single step.
    def step(self):
        self.interact()
        self.reproduce()

    # Manages interactions with neighboring agents.
    def interact(self):
        # Get coordinates of existing neighbors only
        neighbors_coords = self.model.get_neighbors(self.pos, moore=False, all=False)
        # Retrieve agent objects from coordinates
        neighbors = [self.model.grid.get(pos) for pos in neighbors_coords]
        for other_agent in neighbors:
            # Check if the current agent is in an affluent area
            affluent = self.model.is_affluent_area(self.pos)

            # Adjust interaction costs and gains if in an affluent area
            cost_of_giving = param.COST_OF_GIVING / 2 if affluent else param.COST_OF_GIVING
            gain_of_receiving = param.GAIN_OF_RECEIVING * 2 if affluent else \
                param.GAIN_OF_RECEIVING

            if self.color == other_agent.color:
                if self.cooperate_with_same:
                    if self.ptr - cost_of_giving >= 0:
                        self.ptr -= cost_of_giving
                        other_agent.ptr += gain_of_receiving
            else:
                if self.cooperate_with_different:
                    if self.ptr - cost_of_giving >= 0:
                        self.ptr -= cost_of_giving
                        other_agent.ptr += gain_of_receiving

    # Determines if reproduction occurs.
    def reproduce(self):
        # Use the agent's reproductive potential (ptr) as the probability of reproduction
        if random.random() < self.ptr:
            # Get coordinates of all neighboring positions
            neighbor_all_coords = set(self.model.get_neighbors(self.pos, moore=False, all=True))
            neighbor_coords = set(self.model.get_neighbors(self.pos, moore=False, all=False))
            # Find coordinates of empty neighboring cells
            empty_cells = list(neighbor_all_coords - neighbor_coords)
            if empty_cells:  # If there are empty spots
                new_pos = random.choice(empty_cells)
                # Create agent, considering mutation
                new_agent = EthnocentrismAgent(
                    unique_id=self.model.next_id(),
                    model=self.model,
                    color=self.mutate_color(self.color),  # Color may mutate
                    # Cooperation strategy may mutate
                    cooperate_with_same=self.mutate_strategy(self.cooperate_with_same),
                    # Cooperation strategy may mutate
                    cooperate_with_different=self.mutate_strategy(self.cooperate_with_different),
                    pos=new_pos  # Position of the new agent
                )

                self.model.grid[new_pos] = new_agent
                self.model.schedule.append(new_agent)

    # Mutates the agent's color.
    def mutate_color(self, color):
        # Simple example: small chance to change color
        if random.random() < param.MUTATION_RATE:  # Mutation rate
            return random.choice(param.RANDOM_COLOR)
        else:
            return color

    # Mutates the agent's cooperation strategy.
    def mutate_strategy(self, strategy):
        # Simple example: small chance to change strategy
        if random.random() < param.MUTATION_RATE:  # Mutation rate
            return not strategy
        else:
            return strategy
