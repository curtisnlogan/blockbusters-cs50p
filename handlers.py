from datetime import date

import cli
from rental_record import RentalRecord
import startup_reconciliation
import sys


def handle(data: dict) -> dict:
    """
    Calls the CLI, handles data mutation from the CLI, and returns a dictionary with the results.
    """
    # Call the reconcile function first to perform necessary startup checks
    # Default can be set to "rentals" or any other relevant target in the data dictionary
    # The 'today' parameter is set to the current date for accurate reconciliation.
    # It should also pass today as a parameter to class modules that require it for their own logic,
    # ensuring a consistent date reference across the application.
    data = startup_reconciliation.reconcile(data, target="rentals", today=date.today())

    # call cli main_menu function to allow for data mutation from the user
    while True:
        try:
            selection = cli.main_menu()
        except ValueError as e:
            print(e)
            continue
        if selection == "1":
            game_records = data["game_records"]
            cli.view_game_records(game_records)
        if selection == "2":
            members = data["members"]
            cli.view_members(members)
        if selection == "3":
            try:
                rentals_choice = cli.rentals_management()
            except ValueError as e:
                print(e)
            if rentals_choice == "1":
                rentals = data["rentals"]
                try:
                    new_rentals = cli.rent_games(rentals)
                    new_rentals = generate_new_rentals(data, new_rentals)
                except (ValueError, KeyError) as e:
                    print(e)
                    continue  # Return to the main menu if there's an error
            elif rentals_choice == "2":
                rentals = data["rentals"]
                cli.return_games(rentals)
            elif rentals_choice == "3":
                rentals = data["rentals"]
                cli.pay_fees(rentals)
            elif rentals_choice == "4":
                continue  # Return to the main menu
        if selection == "4":
            sys.exit()  # Exit the program
    
def generate_new_rentals(data:dict, new_rentals: tuple) -> list:
    """
    Generates new rental instances based on the provided Game IDs and Member ID.
    Updates the total copies of the games in the in-memory data store.
    Returns a list of new RentalRecord instances.
    """
    member_id = new_rentals[1]
    new_rental_instances = []
    for game_id in new_rentals[0]:
        new_rental_instances.append(RentalRecord(game_id, member_id))
        data["game_records"][game_id]["total_copies"] -= 1

    return new_rental_instances

