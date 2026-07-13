from datetime import date
import sys

import cli
import startup_reconciliation


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
            cli.main_menu()  # Prompt the user again if they entered an invalid choice
        if selection == "1":
            if data.get("game_records") is None:
                raise KeyError(
                    "Game records data is missing. Please ensure the data is loaded correctly."
                )
            game_records = data.get("game_records")
            cli.view_game_records(game_records)
        if selection == "2":
            if data.get("members") is None:
                raise KeyError(
                    "Members data is missing. Please ensure the data is loaded correctly."
                )
            members = data.get("members")
            cli.view_members(members)
        if selection == "3":
            if data.get("rentals") is None:
                raise KeyError(
                    "Rentals data is missing. Please ensure the data is loaded correctly."
                )
            rentals = data.get("rentals")
            cli.rentals_menu(rentals)
        if selection == "4":
            sys.exit()

    return data
