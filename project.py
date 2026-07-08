import config
import storage

def main():
    # dict defines the paths to the json files for each storage type
    storage_dict = {
        "game_records": config.GAME_RECORDS_PATH,
        "members": config.MEMBERS_PATH,
        "rentals": config.RENTALS_PATH,
        }
    
    in_memory_storage = storage.load_jsons(**storage_dict)


if __name__ == "__main__":
    main()
