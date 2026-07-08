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
    
    in_memory_storage = storage.load_jsons(**storage_dict)

    # call the handler function to allow for data mutation from the user
    in_memory_storage = handlers.handle(in_memory_storage)


if __name__ == "__main__":
    main()
