import matplotlib.pyplot as plt
import matplotlib.animation as animation
from pymongo import MongoClient
import os
import dotenv

dotenv.load_dotenv()
# **MongoDB 连接信息**

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = "mouse_tracker"
COLLECTION_NAME = "mouse_events"

# **连接 MongoDB**
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

def fetch_mouse_trajectories(os_name=None, limit=10):
    """ 从 MongoDB 拉取鼠标轨迹数据 """
    query = {}
    if os_name:
        query["os_name"] = os_name  # 按操作系统筛选数据

    # 获取鼠标点击事件
    cursor = collection.find(query).sort("click_time", -1).limit(limit)
    return list(cursor)

def play_mouse_trajectory(trajectory, click_time):
    """ 播放单个鼠标轨迹 """

    # 提取轨迹数据
    x = [point["x"] for point in trajectory]
    y = [point["y"] for point in trajectory]
    click_indices = [i for i, point in enumerate(trajectory) if "action" in point and point["action"] == "Click"]

    fig, ax = plt.subplots()
    ax.set_xlim(min(x) - 50, max(x) + 50)
    ax.set_ylim(min(y) - 50, max(y) + 50)
    ax.invert_yaxis()
    line, = ax.plot([], [], "bo-", alpha=0.6)

    # 起点（红色）
    ax.plot(x[0], y[0], "ro", label="Start")

    # 点击点（绿色）
    if click_indices:
        ax.plot([x[i] for i in click_indices], [y[i] for i in click_indices], "go", label="Click Point")

    ax.set_title(f"Mouse Trajectory - Click Time: {click_time}")
    ax.legend()

    # **动画初始化**
    def init():
        line.set_data([], [])
        return line,

    # **更新轨迹**
    def update(frame):
        line.set_data(x[:frame], y[:frame])
        return line,

    # **创建动画**
    ani = animation.FuncAnimation(fig, update, frames=len(x), init_func=init, interval=50, blit=True)

    # 显示动画
    plt.show(block=True)

def replay_from_mongodb(os_name=None, limit=5):
    """ 读取 MongoDB 数据并逐个回放 """
    trajectories = fetch_mouse_trajectories(os_name, limit)

    if not trajectories:
        print("No mouse trajectory data found.")
        return

    for traj in trajectories:
        print(f"Playing trajectory from {traj['click_time']} ({traj['os_name']})")
        play_mouse_trajectory(traj["trajectory"], traj["click_time"])

if __name__ == "__main__":
    replay_from_mongodb(os_name=None, limit=5)  # 可修改 os_name="macos" 只回放 Mac 轨迹
