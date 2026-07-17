import json
import os


def load_json(**kwargs) -> dict:
    """
    Load data through key-value pairs where the key is the name of the data
    and the value is the path to the json file.
    """
    in_memory_data = {}
    for key, value in kwargs.items():
        with open(value, "r") as f:
            in_memory_data[key] = json.load(f)
    return in_memory_data


def save_json(**kwargs: dict) -> None:
    """
    Save data through key-value pairs where the key is the name of the data
    and the value is the data itself, which must be a Python dict.
    The data will be saved as a JSON file with the name of the key.
    Note: This function will overwrite existing files with the same name without warning.
    """
    for key, value in kwargs.items():
        if not isinstance(value, dict):
            raise TypeError(
                f"Error: {value} is not a Python dict."
                f"Only Python dicts should be saved to storage."
                f"Please check the value for key: {key}"
            )

    for key, value in kwargs.items():
        """
        Save the data to a temporary JSON file first, then rename it to the final name.
        This approach helps prevent data loss in case of an error during the save process.
        """
        with open(f"data/{key}.json.tmp", "w") as f:
            json.dump(value, f)

        # Rename the temporary file to the final name, replacing the old file if it exists.
        # This is practically atomic for this project, which helps prevent data loss.
        os.replace(f"data/{key}.json.tmp", f"data/{key}.json")
