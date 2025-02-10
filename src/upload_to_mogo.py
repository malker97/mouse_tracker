import os
import pandas as pd
from pymongo import MongoClient
import platform

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

def process_csv(file_path):
    """ 读取 CSV 文件并转换为 MongoDB 文档格式 """
    df = pd.read_csv(file_path)

    if df.empty:
        print(f"Skipping empty file: {file_path}")
        return None

    os_name = platform.system().lower()
    click_row = df[df["Action"] == "Click"] if "Action" in df.columns else None
    click_time = float(click_row.iloc[0]["Timestamp"]) if not click_row.empty else df.iloc[0]["Timestamp"]

    document = {
        "os_name": os_name,
        "click_time": click_time,
        "trajectory": []
    }

    for _, row in df.iterrows():
        point = {
            "timestamp": float(row["Timestamp"]),
            "x": float(row["X"]),
            "y": float(row["Y"])
        }
        if "Action" in row and isinstance(row["Action"], str):
            point["action"] = row["Action"]

        document["trajectory"].append(point)

    return document

def upload_single_csv(file_path):
    """ 上传单个 CSV 文件到 MongoDB，并在成功后删除 """
    document = process_csv(file_path)
    if document:
        collection.insert_one(document)
        print(f"Uploaded {file_path} to MongoDB.")
        os.remove(file_path)  # **上传成功后删除文件**
        print(f"Deleted {file_path}")

if __name__ == "__main__":
    print("This script is meant to be imported and used in mouse_tracker.py.")
