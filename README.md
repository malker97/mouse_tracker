# Mouse Tracker and Replay

这个项目包含两个主要功能：鼠标轨迹记录和鼠标轨迹回放。

# 鼠标轨迹记录
## 安装依赖

首先，确保你已经安装了项目所需的依赖。你可以使用以下命令安装：
```bash
pip install -r requirements.txt
```

## 运行
运行 mouse_tracker.py 来记录鼠标点击前后各 1 秒的轨迹数据。数据将会保存在 mouse_clicks 目录下。

## 回放鼠标轨迹
运行 replay.py 来回放记录的鼠标轨迹数据。程序会自动播放 mouse_clicks 目录下的所有轨迹文件。

文件说明
mouse_tracker.py：用于记录鼠标点击前后各 1 秒的轨迹数据。
replay.py：用于回放记录的鼠标轨迹数据。
requirements.txt：项目所需的依赖包列表。
mouse_clicks：存储鼠标轨迹数据的目录。
