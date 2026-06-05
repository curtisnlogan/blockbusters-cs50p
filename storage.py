import json
from pathlib import Path


def load_jsons(**kwargs) -> dict:
    """
    Load data through key-value pairs where the key is the name of the data
    and the value is the path to the json file.
    """
    in_memory_data = {}
    for key, value in kwargs.items():
        if Path(value).is_file():
            with open(value, "r") as f:
                try:
                    in_memory_data[key] = json.load(f)
                except json.JSONDecodeError as e:
                    raise ValueError(f"Error not parsing JSON from {value}")
        else:
            raise FileNotFoundError(f"File not found: {value}")
    return in_memory_data
