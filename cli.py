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
                f"Error: Invalid {game_id} or {member_id}. Please check your input and try again."
            )
        break  # Exit the loop if both IDs are valid

    console.print(
        f"Processing rental for Game ID: {game_id} and Member ID: {member_id}."
    )
    console.print(
        'Read to the member: "For each day the game is late, a flat fee of $1 will be charged.'
        "If the game is returned more than 14 days late,"
        'the member will be charged a flat fee of $40 for the replacement cost of the game."'
    )
    while True:
        confirm_read = (
            input(
                "Do you confirm that the member has read and understood this? Enter 'y' to confirm"
            )
            .strip()
            .lower()
        )
        if confirm_read == "y":
            return game_id, member_id
        else:
            console.print(
                "Please ensure the member reads and understands the rental terms before proceeding."
            )
            continue  # Prompt again if the member has not confirmed understanding


def return_games(data: dict):
    # Implement the logic for returning a game here
    pass


def pay_fees(data: dict):
    # Implement the logic for paying fees here
    pass
