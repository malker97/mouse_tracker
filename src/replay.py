import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pandas as pd
import os
import glob

# 读取所有 click_*.csv 文件，按文件名排序
click_files = sorted(glob.glob("./mouse_clicks/*_click_*.csv"))

# 如果没有文件，退出
if not click_files:
    print("No mouse click data found in mouse_clicks/")
    exit()

def play_mouse_trajectory(file):
    """ 播放单个 CSV 轨迹 """
    df = pd.read_csv(file)

    x = df["X"]
    y = df["Y"]
    click_indices = df[df["Action"] == "Click"].index

    fig, ax = plt.subplots()
    ax.set_xlim(min(x) - 50, max(x) + 50)
    ax.set_ylim(min(y) - 50, max(y) + 50)
    ax.invert_yaxis()  # 让 y 轴方向符合屏幕坐标
    line, = ax.plot([], [], "bo-", alpha=0.6)
    star_point = ax.plot(x[0], y[0], "ro")  # 显示起始点
    end_point = ax.plot(x[click_indices], y[click_indices], "go")  # 显示结束点
    # 显示标题
    ax.set_title(f"Mouse Trajectory - {os.path.basename(file)}")

    # 初始化函数
    def init():
        line.set_data([], [])
        return line,

    # 更新函数
    def update(frame):
        line.set_data(x[:frame], y[:frame])
        return line,

    # 运行动画

    ani = animation.FuncAnimation(fig, update, frames=len(x), init_func=init, interval=50, blit=True)

    # 显示窗口并等待动画播放完
    plt.show(block=True)

# **自动播放所有轨迹**
for file in click_files:
    print(f"Playing: {file}")
    play_mouse_trajectory(file)  # 播放当前轨迹，动画结束后自动播放下一个