import pandas as pd
import matplotlib.pyplot as plt

# Plots agent data from a CSV file showing cooperation over time.
def plot_agent_data(csv_file):
    # Read CSV file
    data = pd.read_csv(csv_file)

    # Set the figure size and resolution
    plt.figure(figsize=(10, 6), dpi=80)

    # Plot line charts for each agent type
    plt.plot(data['Step'], data['CC'], label='CC', color='green', linewidth=2)
    plt.plot(data['Step'], data['CD'], label='CD', color='red', linewidth=2)
    plt.plot(data['Step'], data['DC'], label='DC', color='yellow', linewidth=2)
    plt.plot(data['Step'], data['DD'], label='DD', color='black', linewidth=2)

    # Add title and labels
    plt.title('Agent Cooperation Over Time')
    plt.xlabel('Simulation Step')
    plt.ylabel('Number of Agents')

    # Display the legend
    plt.legend()

    # Display grid
    plt.grid(True)

    # Save the image or display the plot
    plt.savefig('agent_cooperation.png')  # Save to file
    plt.show()  # Display the plot


if __name__ == '__main__':
    # Specify the path to the CSV file
    csv_file = 'agent_stats.csv'
    plot_agent_data(csv_file)
