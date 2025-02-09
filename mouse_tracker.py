import time
import csv
import os
from collections import deque
from pynput import mouse

# 配置参数
buffer_duration = 1.0  # 记录点击前 1 秒和后 1 秒的数据
save_directory = "mouse_clicks"  # 存储所有子表格
click_count = 0  # 记录点击次数

# 创建存储目录
if not os.path.exists(save_directory):
    os.makedirs(save_directory)

# 维护滑动窗口
mouse_buffer = deque()
is_recording_after_click = False
after_click_start_time = None
click_events = []

# 监听鼠标移动
def on_move(x, y):
    global is_recording_after_click, after_click_start_time

    timestamp = time.time()
    
    # 只保留 buffer_duration 内的移动数据（点击前 1 秒）
    mouse_buffer.append((timestamp, x, y))
    
    # 移除超过 buffer_duration 以前的数据
    while mouse_buffer and timestamp - mouse_buffer[0][0] > buffer_duration:
        mouse_buffer.popleft()

    # 记录点击后的数据
    if is_recording_after_click:
        click_events.append((timestamp, x, y))
        if timestamp - after_click_start_time > buffer_duration:
            is_recording_after_click = False  # 停止记录

# 监听鼠标点击
def on_click(x, y, button, pressed):
    global is_recording_after_click, after_click_start_time, click_count

    timestamp = time.time()

    if pressed:  # 仅记录鼠标按下的瞬间
        click_count += 1
        print(f"Mouse Clicked at ({x}, {y}) at {timestamp}")

        # 复制点击前的 1 秒数据
        click_data = list(mouse_buffer)

        # 记录点击事件
        click_data.append((timestamp, x, y, "Click"))

        # 开始记录点击后的 1 秒数据
        is_recording_after_click = True
        after_click_start_time = timestamp
        click_events.clear()

        # 延迟 1 秒后保存数据
        time.sleep(1.1)  # 确保后续数据已经收集

        # 生成文件路径
        filename = os.path.join(save_directory, f"click_{click_count}.csv")

        # 保存点击前后的数据
        save_to_csv(filename, click_data + click_events)

# 保存数据到 CSV（每次点击单独存储）
def save_to_csv(filename, data):
    with open(filename, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Timestamp", "X", "Y", "Action"])
        for row in data:
            writer.writerow(row)
    
    print(f"Saved click data to {filename} ({len(data)} rows)")

# 启动监听器
def start_tracking():
    with mouse.Listener(on_move=on_move, on_click=on_click) as listener:
        print("Tracking started. Recording 1s before and after each click...")
        listener.join()

if __name__ == "__main__":
    start_tracking()
