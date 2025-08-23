import json
import os

from .config import storage_data_path as data_path

# Storage is a big dict in a JSON format
# It is accessed through period-separated keys
# EX. "levels.0-0.best_score"
data: dict = {}


class StorageError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return self.message

def load_data():
    global data
    if not os.path.exists(data_path):
        print("Storage file doesn't exist. Creating one.")
        open(data_path, "w+").close()
    else:
        try:
            raw_data = open(data_path, "r").read()
            data = json.loads(raw_data)
        except:
            raise StorageError(f"Failed to load the storage JSON file at {data_path}")

def save_data():
    open(data_path, "w").write(json.dumps(data))

def set(key: str, value: str | int | float):
    d = data
    key_parts = key.split(".")
    for i, key_part in enumerate(key_parts):
        if key_part not in d:
            if i == len(key_parts) - 1:
                d[key_part] = value
                return
            else:
                d[key_part] = {}
        d = d[key_part]

def get(key: str) -> str | int | float | dict | None:
    d = data
    key_parts = key.split(".")
    for key_part in key_parts:
        if key_part not in d:
            return None
        d = d[key_part]
    return d