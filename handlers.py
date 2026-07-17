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
    today = date.today()
    data = startup_reconciliation.reconcile(data, today, target="rentals")

    # call cli main_menu function to allow for data mutation from the user
    while True:
        try:
            selection = cli.main_menu()
        except ValueError as e:
            print(e)
            continue
        if selection == "1":
            game_records = data["game_records"]
            # awaits user input to return to the main menu after viewing game records
            while True:
                return_menu = cli.view_game_records(game_records)
                if return_menu:
                    break
        if selection == "2":
            members = data["members"]
            cli.view_members(members)
        if selection == "3":
            try:
                rentals_choice = cli.rentals_management()
            except ValueError as e:
                print(e)
            if rentals_choice == "1":
                try:
                    new_rentals = cli.rent_games(data)
                    new_rentals = generate_new_rentals(data, new_rentals)
                    add_new_rentals(data, new_rentals)
                except (ValueError, KeyError) as e:
                    print(e)
                    continue  # Return to the main menu if there's an error
            elif rentals_choice == "2":
                try:
                    returned_games = cli.return_games(data)
                    process_returned_games(data, returned_games)
                    # add a message to the user confirming the successful return in cli.py
                    # not one god success message function
                except (ValueError, KeyError) as e:
                    print(e)
                    continue  # Return to the main menu if there's an error
            elif rentals_choice == "3":
                try:
                    rentals_paid, member_id = cli.pay_fees(data)
                    if rentals_paid:
                        process_paid_fees(data, rentals_paid, member_id)
                    else:
                        continue  # Return to the main menu if no rentals were paid
                except (ValueError, KeyError) as e:
                    print(e)
                    continue  # Return to the main menu if there's an error
            elif rentals_choice == "4":
                continue  # Return to the main menu
        if selection == "4":
            sys.exit()  # Exit the program


def generate_new_rentals(data: dict, new_rentals: tuple) -> list:
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


def add_new_rentals(data: dict, new_rentals: list[RentalRecord]) -> None:
    """
    Adds new rental instances to the in-memory data store.
    Returns None. This function mutates the data dictionary in place.
    """
    for rental_record in new_rentals:
        data["rentals"][rental_record.rental_id] = {
            "rental_id": rental_record.rental_id,
            "membership_id": rental_record.membership_id,
            "game_id": rental_record.game_id,
            "date_rented": rental_record.date_rented,
            "due_for_return": rental_record.due_for_return,
            "late_fees_total": rental_record.late_fees_total,
            "replacement_charge": rental_record.replacement_charge,
            "return_status": rental_record.return_status,
        }

    cli.success_message("The rental(s) have been officially added to the system.")


def process_returned_games(data: dict, returned_games: list) -> None:
    """
    Processes returned games by updating their return status and the total copies of the games.
    Returns None. This function mutates the data dictionary in place.
    """
    for returned_game in returned_games:
        game_id = data["rentals"][returned_game]["game_id"]
        data["rentals"][returned_game] = {"return_status": "returned"}
        data["game_records"][game_id]["total_copies"] += 1

    cli.success_message("The rental(s) have been officially returned in the system.")


def process_paid_fees(data: dict, rentals_paid: set, member_id: str) -> None:
    for rental in rentals_paid:
        if data["rentals"][rental]["replacement_charge"]:
            data["rentals"][rental]["replacement_charge"] = False
            data["members"][member_id]["account_status"] = True
        else:
            data["rentals"][rental]["late_fees_total"] = 0.0
            data["rentals"][rental]["return_status"] = "returned"
            data["members"][member_id]["account_status"] = True

    cli.success_message(
        f"Member {data['members'][member_id]['full_name']}'s account has been updated to reflect the payment of fees."
    )
