import pandas as pd
import matplotlib.pyplot as plt

def plot_agent_data(csv_file):
    # Read CSV file
    data = pd.read_csv(csv_file)

    # Create a chart with two subplots, each with its own axes
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 12), dpi=80)  # Two subplots, vertical layout

    # Plot data for the left area on the first subplot
    ax1.plot(data['Step'], data['L_CC'], label='L_CC', color='green', linewidth=2)
    ax1.plot(data['Step'], data['L_CD'], label='L_CD', color='red', linewidth=2)
    ax1.plot(data['Step'], data['L_DC'], label='L_DC', color='yellow', linewidth=2)
    ax1.plot(data['Step'], data['L_DD'], label='L_DD', color='black', linewidth=2)
    ax1.set_title('Agent Cooperation Over Time (Left Area)')
    ax1.set_xlabel('Simulation Step')
    ax1.set_ylabel('Number of Agents')
    ax1.legend()
    ax1.grid(True)

    # Plot data for the right area on the second subplot
    ax2.plot(data['Step'], data['R_CC'], label='R_CC', color='green', linewidth=2)
    ax2.plot(data['Step'], data['R_CD'], label='R_CD', color='red', linewidth=2)
    ax2.plot(data['Step'], data['R_DC'], label='R_DC', color='yellow', linewidth=2)
    ax2.plot(data['Step'], data['R_DD'], label='R_DD', color='black', linewidth=2)
    ax2.set_title('Agent Cooperation Over Time (Right Area - Affluent)')
    ax2.set_xlabel('Simulation Step')
    ax2.set_ylabel('Number of Agents')
    ax2.legend()
    ax2.grid(True)

    # Adjust subplot spacing
    plt.tight_layout()

    # Save the image or display the plot
    plt.savefig('agent_cooperation_comparison.png')  # Save to file
    plt.show()  # Display the plot

if __name__ == '__main__':
    # Specify the path to the CSV file
    csv_file = 'agent_stats.csv'
    plot_agent_data(csv_file)
