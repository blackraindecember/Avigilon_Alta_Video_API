import json
import os

def load_config(path="config.json"):

    if not os.path.exists(path):
        raise FileNotFoundError("config.json not found")

    with open(path, "r", encoding="utf-8") as f:
        config = json.load(f)

    required = ["base_url", "username", "password"]

    for key in required:
        if key not in config:
            raise ValueError(f"Missing '{key}' in config.json")

    return config
