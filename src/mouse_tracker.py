import time
import csv
import os
import threading
from collections import deque
from pynput import mouse
import platform

from upload_to_mogo import upload_single_csv

# 配置参数
buffer_duration = 1.0  # 记录点击前 1 秒和后 1 秒的数据
sampling_interval = 1 / 100  # 控制采样率
save_directory = "mouse_clicks"
click_count = 0
last_sample_time = 0
os_name = platform.system().lower()

# 创建存储目录
if not os.path.exists(save_directory):
    os.makedirs(save_directory)

# 维护滑动窗口
mouse_buffer = deque()
is_recording_after_click = False
after_click_start_time = None
click_events = []

def on_move(x, y):
    global is_recording_after_click, after_click_start_time, last_sample_time

    timestamp = time.time()
    if timestamp - last_sample_time < sampling_interval:
        return  # 限制采样频率
    
    last_sample_time = timestamp
    mouse_buffer.append((timestamp, x, y))

    while mouse_buffer and timestamp - mouse_buffer[0][0] > buffer_duration:
        mouse_buffer.popleft()

    if is_recording_after_click:
        click_events.append((timestamp, x, y))
        if timestamp - after_click_start_time > buffer_duration:
            is_recording_after_click = False

def on_click(x, y, button, pressed):
    global is_recording_after_click, after_click_start_time, click_count

    timestamp = time.time()

    if pressed:  # 仅记录鼠标按下
        click_count += 1
        print(f"Mouse Clicked at ({x}, {y}) at {timestamp}")

        click_data = list(mouse_buffer)
        click_data.append((timestamp, x, y, "Click"))

        is_recording_after_click = True
        after_click_start_time = timestamp
        click_events.clear()

        # **后台线程处理数据**
        threading.Thread(target=delayed_save_and_upload, args=(click_data,)).start()

def delayed_save_and_upload(click_data):
    """ 等待 1 秒收集数据，保存 CSV，然后上传到 MongoDB 并删除 CSV """
    global click_events

    time.sleep(1.1)
    full_click_data = click_data + click_events

    filename = os.path.join(save_directory, f"{os_name}_click_{click_count}.csv")

    save_to_csv(filename, full_click_data)

    # **上传到 MongoDB 并删除 CSV**
    upload_single_csv(filename)

def save_to_csv(filename, data):
    with open(filename, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Timestamp", "X", "Y", "Action"])
        for row in data:
            writer.writerow(row)
    
    print(f"Saved {filename} ({len(data)} rows)")

def start_tracking():
    with mouse.Listener(on_move=on_move, on_click=on_click) as listener:
        print("Tracking started. Recording 1s before and after each click...")
        listener.join()

if __name__ == "__main__":
    start_tracking()
