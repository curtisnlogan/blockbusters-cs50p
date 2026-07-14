from datetime import date

import cli
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
                cli.rent_games(rentals)
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
