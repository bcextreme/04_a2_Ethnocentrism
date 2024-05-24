import csv
import random
import param
from agent import EthnocentrismAgent


class EthnocentrismModel:
    # Initializes the model.
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

        # Use integers for real-time counting
        self.agent_count_dict = {'CC': 0, 'CD': 0, 'DC': 0, 'DD': 0}
        self.csv_file_stats = open('agent_stats.csv', mode='w', newline='', encoding='utf-8')
        self.csv_writer_stats = csv.writer(self.csv_file_stats)
        self.csv_writer_stats.writerow(["Step", "CC", "CD", "DC", "DD"])

        self.csv_file = open('model_output.csv', mode='w', newline='', encoding='utf-8')
        self.csv_writer = csv.writer(self.csv_file)
        self.csv_writer.writerow(
            ["UniqueID", "PosX", "PosY", "Color", "CooperateWithSame", "CooperateWithDifferent", "Step"])

    # Simulates one step in the model.
    def step(self):
        self.record_agents_state()
        self.step_count += 1
        empty_cells = len([pos for pos, agent in self.grid.items() if agent is None])

        num_new_agents = min(param.IMMIGRANTS_PER_DAY, empty_cells)
        for _ in range(num_new_agents):
            # Assign a new unique ID based on the current schedule size
            self.create_agent()

        random.shuffle(self.schedule)
        for agent in self.schedule:
            agent.step()

        self.death()

        for key in self.agent_count_dict.keys():
            self.agent_count_dict[key] = 0

        for agent in self.schedule:
            key = (('C' if agent.cooperate_with_same else 'D')
                   + ('C' if agent.cooperate_with_different else 'D'))
            self.agent_count_dict[key] += 1

        self.record_agent_counts()

    # Creates a new agent.
    def create_agent(self):
        empty_cells = [k for k, v in self.grid.items() if v is None]
        if not empty_cells:
            return

        pos = random.choice(empty_cells)
        color = random.choice(param.RANDOM_COLOR)
        cooperate_with_same = (random.random()
                               < param.IMMIGRANT_CHANCE_COOPERATE_WITH_SAME)
        cooperate_with_different = (random.random()
                                    < param.IMMIGRANT_CHANCE_COOPERATE_WITH_DIFFERENT)

        agent = EthnocentrismAgent(
            unique_id=self.next_id(),
            model=self,
            color=color,
            cooperate_with_same=cooperate_with_same,
            cooperate_with_different=cooperate_with_different,
            pos=pos  # This line also passes the position to the agent
        )

        self.grid[pos] = agent
        self.schedule.append(agent)

    # Returns a list of neighbors.
    def get_neighbors(self, pos, moore=False, all=False):
        directions = [
            (-1, 0),  # Left
            (1, 0),  # Right
            (0, -1),  # Down
            (0, 1),  # Up
        ]

        if moore:
            directions += [
                (-1, -1),  # Bottom Left
                (-1, 1),  # Top Left
                (1, -1),  # Bottom Right
                (1, 1),  # Top Right
            ]

        neighbors = []
        for dx, dy in directions:
            x, y = pos[0] + dx, pos[1] + dy

            if 0 <= x < self.grid_width and 0 <= y < self.grid_height:
                if all:  # Return all positions
                    neighbors.append((x, y))
                else:  # Return positions only if they are occupied
                    if self.grid.get((x, y)) is not None:
                        neighbors.append((x, y))

        return neighbors

    # Handles agent death.
    def death(self):
        random.shuffle(self.schedule)  # Shuffle the list
        alive_agents = []
        for agent in self.schedule:
            if random.random() >= param.DEATH_RATE:
                alive_agents.append(agent)
            else:
                self.grid[agent.pos] = None  # Mark the agent's cell as empty
        self.schedule = alive_agents

    # Generates an ID for a new agent.
    def next_id(self):
        self.current_id += 1
        return self.current_id - 1

    # Records the state of each agent at the current step in a CSV file.
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

    # Logs the counts of agent interactions by type at each step and flushes to CSV.
    def record_agent_counts(self):
        counts = [self.agent_count_dict['CC'], self.agent_count_dict['CD'],
                  self.agent_count_dict['DC'], self.agent_count_dict['DD']]
        self.csv_writer_stats.writerow([self.step_count] + counts)
        self.csv_file_stats.flush()  # Force flush writing

    # Closes statistical output files.
    def close_files(self):
        self.csv_file_stats.close()

    # Ensures files are closed properly.
    def __del__(self):
        self.csv_file.close()
        self.csv_file_stats.close()
