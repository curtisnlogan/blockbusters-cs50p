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


def save_jsons(**kwargs: dict[str, dict]) -> None:
    """
    Save data through key-value pairs where the key is the name of the data
    and the value is the data itself, which must be a Python dict.
    The data will be saved as a JSON file with the name of the key.
    Note: This function will overwrite existing files with the same name without warning.
    """
    for key, value in kwargs.items():
        if isinstance(value, dict):
            with open(f"data/{key}.json", "w") as f:
                json.dump(value, f)
        else:
            raise ValueError(
                f"Error: {value} is not a Python dict. "
                f"Only Python dicts can be dumped to JSON. "
                f"Please check the value for key: {key}"
            )
