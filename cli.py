from rich.console import Console
from rich.table import Table

# Rich's main output object
# Detects terminal capabilities (width, color) and adapts formatting
console = Console()


def main_menu() -> str:
    """
    Displays the main menu and prompts the user for input.
    Returns the user's choice as a string.
    """
    while True:
        console.print(
            "\nWelcome to the Blockbusters CLI! All data has been successfully loaded into memory."
            "Please select an option from the menu below:"
        )
        console.print("\nMain Menu:")
        console.print("1. View Game Records")
        console.print("2. View Members")
        console.print("3. Rentals Management")
        console.print("4. Exit the Program and Save Changes")

        main_choice = input("Enter your choice (1–4): ")
        if main_choice not in ["1", "2", "3", "4"]:
            raise ValueError(
                "Invalid choice. Please enter a number exactly between 1 and 4."
            )
        elif main_choice == "1":
            console.print("You selected Game Records.")
            return main_choice
        elif main_choice == "2":
            console.print("You selected Members.")
            return main_choice
        elif main_choice == "3":
            console.print("You selected Rentals.")
            return main_choice
        elif main_choice == "4":
            confirm_exit = (
                input("Are you sure you want to exit? (y/n): ").strip().lower()
            )
            if confirm_exit == "y":
                console.print("Exiting the program and saving changes.")
                return main_choice
            else:
                continue  # Return to the main menu if the user does not confirm exit

def success_message(message: str):
    """
    Displays a success message to the user.
    """
    console.print(f"\n[bold green]Success:[/bold green] {message}\n")


def view_game_records(game_records: dict):

    # create a table to display game records
    table = Table(title="Game Records")

    # define columns
    table.add_column("Game ID", justify="right")
    table.add_column("Title", justify="right")
    table.add_column("Platform", justify="right")
    table.add_column("Total Copies", justify="right")
    table.add_column("Replacement Cost", justify="right")

    # build rows
    for game in game_records:
        table.add_row(
            game["game_id"],
            game["title"],
            game["platform"],
            str(game["total_copies"]),
            str(game["replacement_cost"]),
        )

    # end
    console.print(table)


def view_members(members: dict):
    # create a table to display member information
    table = Table(title="Members")

    # define columns
    table.add_column("Member ID", justify="right")
    table.add_column("Full Name", justify="right")
    table.add_column("Is Over 18", justify="right")
    table.add_column("Address", justify="right")
    table.add_column("Payment Method", justify="right")
    table.add_column("Account Status", justify="right")

    # build rows from dict
    for member in members:
        table.add_row(
            member["member_id"],
            member["full_name"],
            str(member["is_over_18"]),
            member["address"],
            member["payment_method"],
            str(member["account_status"]),
        )

    # output the table to the console
    console.print(table)


def rentals_management() -> str:
    """
    Sub-menu allows user to choose between renting games, returning games and paying fees.
    Returns a string indicating the choice made by the user.
    """
    while True:
        console.print("\nRentals Management Menu:")
        console.print("1. Rent Games")
        console.print("2. Return Games")
        console.print("3. Pay Fees")
        console.print("4. Back to Main Menu\n")

        rentals_choice = input("Enter your choice (1-4): ").strip()
        if rentals_choice not in ["1", "2", "3", "4"]:
            raise ValueError(
                "Invalid choice. Please enter a number exactly between 1 and 4."
            )
        elif rentals_choice == "1":
            console.print("You selected Rent Games.")
            return rentals_choice
        elif rentals_choice == "2":
            console.print("You selected Return Games.")
            return rentals_choice
        elif rentals_choice == "3":
            console.print("You selected Pay Fees.")
            return rentals_choice
        elif rentals_choice == "4":
            confirm_exit = (
                input("Are you sure you want to go back to the main menu? (y/n): ")
                .strip()
                .lower()
            )
            if confirm_exit == "y":
                console.print("Returning to the main menu.")
                return rentals_choice
            else:
                continue  # Return to the rentals management menu if the user does not confirm exit


def rent_games(data: dict) -> tuple:
    """
    Handles multiple game rentals by prompting the user for Game IDs and Member ID.
    Validates the inputs and checks for account status and game availability.
    Returns a tuple containing the list of Game IDs and the Member ID."""
    while True:
        game_ids = (
            input("Enter the Game IDs that are to be rented, separated by '/' only: ")
            .strip()
            .lower()
            .split("/")
        )
        member_id = input("Enter the Members ID: ").strip().lower()
        # check if valid member id
        if member_id not in data["members"]:
            raise ValueError(
                f"Error: Invalid {member_id}. Please check your input and try again."
            )
        # check if all game IDs are valid
        if not all(g_id in data["game_records"] for g_id in game_ids):
            raise ValueError(
                "Error: One or more Game IDs are invalid. Please check your input and try again."
            )
        break  # Exit the loop if both IDs are valid
    # check if the member's account is blocked
    if data["members"][member_id]["account_status"] != str(True).lower():
        raise ValueError(
            f"{member_id} has a blocked account. "
            f"Inform the customer that this can be "
            f"rectified through paying all late fees, "
            f"along with any replacement charges."
        )

    for game_id in game_ids:
        if data["game_records"][game_id]["total_copies"] <= 0:
            raise ValueError(
                f"Game ID: {game_id} is currently out of stock. "
                "Politely inform the customer and apologize for the inconvenience. "
                "Suggest they check back later or consider renting a different game."
            )

    console.print(
        f"Read to the customer: For each day the game is late, a flat fee of $1 will be charged. "
        f"If the game is returned more than 14 days late, "
        f"the member will be charged a flat fee of ${data['game_records']['replacement_cost']} "
        f"for the replacement cost of the game."
    )

    while True:
        confirm_read = (
            input(
                "Do you confirm that the member has read and agreed to this? Enter 'y' to confirm"
            )
            .strip()
            .lower()
        )
        if confirm_read == "y":
            break
        else:
            raise ValueError(
                "The customer has not agreed to these terms and the rental(s) cannot proceed."
            )

    console.print(
        f"Valid Rental: Generating rental entry for Game ID: {print(*game_ids, sep=', ', end='')} and Member ID: {member_id}."
    )
    return game_ids, member_id


def return_games(data: dict) -> list:
    """
    Prompts the user for Rental IDs to be returned, validates them
    Returns a list of validated rental IDs.
    """
    while True:
        rental_ids = (
            input(
                "Enter the Rental IDs that are to be returned, separated by '/' only: "
            )
            .strip()
            .lower()
            .split("/")
        )

        # check if all rental IDs are valid
        if not all(r_id in data["rentals"] for r_id in rental_ids):
            raise ValueError(
                "Error: One or more Rental IDs are invalid. Please check your input and try again."
            )
        break  # Exit the loop if rental IDs are valid

    for rental_id in rental_ids:
        if data["rentals"][rental_id]["return_status"] == "returned":
            raise ValueError(f"Rental ID: {rental_id} has already been returned.")
        elif data["rentals"][rental_id]["return_status"] == "lost":
            raise ValueError(
                f"Rental ID: {rental_id} has been reported lost. Please pay the replacement charge to unblock your account."
            )
    return rental_ids


def pay_fees(data: dict):
    # Implement the logic for paying fees here
    pass
