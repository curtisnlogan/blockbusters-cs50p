import json
import sys

import config
import handlers

import storage


def main():
    # dict defines the paths to the json files for each storage type
    storage_dict = {
        "game_records": config.GAME_RECORDS_PATH,
        "members": config.MEMBERS_PATH,
        "rentals": config.RENTALS_PATH,
    }

    try:
        in_memory_storage: dict = storage.load_json(**storage_dict)
    except (json.JSONDecodeError, OSError) as e:
        sys.exit(f"Error: {e}")

    # call the handler function to allow for data mutation from the user
    try:
        in_memory_storage = handlers.handle(in_memory_storage)
    except (KeyError, ValueError) as e:
        sys.exit(f"Error: {e}")
    # a production version would save more frequently (even atomically), but for this project, we will save at the end of the program
    try:
        storage.save_json(**in_memory_storage)
    except (TypeError, OSError, json.JSONDecodeError) as e:
        sys.exit(f"Error: {e}")


if __name__ == "__main__":
    main()
