import pandas as pd
import matplotlib.pyplot as plt

def plot_agent_data(csv_file):
    # 读取CSV文件
    data = pd.read_csv(csv_file)

    # 创建一个带有两个子图的图表，每个子图都有自己的坐标轴
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 12), dpi=80)  # 两个子图，垂直排列

    # 在第一个子图上绘制左边区域的数据
    ax1.plot(data['Step'], data['L_CC'], label='L_CC', color='green', linewidth=2)
    ax1.plot(data['Step'], data['L_CD'], label='L_CD', color='red', linewidth=2)
    ax1.plot(data['Step'], data['L_DC'], label='L_DC', color='yellow', linewidth=2)
    ax1.plot(data['Step'], data['L_DD'], label='L_DD', color='black', linewidth=2)
    ax1.set_title('Agent Cooperation Over Time (Left Area)')
    ax1.set_xlabel('Simulation Step')
    ax1.set_ylabel('Number of Agents')
    ax1.legend()
    ax1.grid(True)

    # 在第二个子图上绘制右边区域的数据
    ax2.plot(data['Step'], data['R_CC'], label='R_CC', color='green', linewidth=2)
    ax2.plot(data['Step'], data['R_CD'], label='R_CD', color='red', linewidth=2)
    ax2.plot(data['Step'], data['R_DC'], label='R_DC', color='yellow', linewidth=2)
    ax2.plot(data['Step'], data['R_DD'], label='R_DD', color='black', linewidth=2)
    ax2.set_title('Agent Cooperation Over Time (Right Area - Affluent)')
    ax2.set_xlabel('Simulation Step')
    ax2.set_ylabel('Number of Agents')
    ax2.legend()
    ax2.grid(True)

    # 调整子图间距
    plt.tight_layout()

    # 保存图像或显示图表
    plt.savefig('agent_cooperation_comparison.png')  # 保存到文件
    plt.show()  # 显示图表

if __name__ == '__main__':
    # 指定CSV文件路径
    csv_file = 'agent_stats.csv'
    plot_agent_data(csv_file)
