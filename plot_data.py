import pandas as pd
import matplotlib.pyplot as plt

def plot_agent_data(csv_file):
    # 读取CSV文件
    data = pd.read_csv(csv_file)

    # 设置图表大小和分辨率
    plt.figure(figsize=(10, 6), dpi=80)

    # 为每种代理类型绘制折线图
    plt.plot(data['Step'], data['CC'], label='CC', linewidth=2)
    plt.plot(data['Step'], data['CD'], label='CD', linewidth=2)
    plt.plot(data['Step'], data['DC'], label='DC', linewidth=2)
    plt.plot(data['Step'], data['DD'], label='DD', linewidth=2)

    # 添加标题和标签
    plt.title('Agent Cooperation Over Time')
    plt.xlabel('Simulation Step')
    plt.ylabel('Number of Agents')

    # 显示图例
    plt.legend()

    # 显示网格
    plt.grid(True)

    # 保存图像或显示图表
    plt.savefig('agent_cooperation.png')  # 保存到文件
    plt.show()  # 显示图表

if __name__ == '__main__':
    # 指定CSV文件路径
    csv_file = 'agent_stats.csv'
    plot_agent_data(csv_file)
