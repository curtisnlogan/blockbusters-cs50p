from rich.console import Console
from rich.table import Table

# Rich's main output object
# Detects terminal capabilities (width, color) and adapts formatting
console = Console()


def main_menu():
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
        console.print("4. Exit the Program")

        choice = input("Enter your choice (1-4): ")
        if choice not in ["1", "2", "3", "4"]:
            raise ValueError(
                "Invalid choice. Please enter a number exactly between 1 and 4."
            )
        elif choice == "1":
            console.print("You selected Game Records.")
            return choice
        elif choice == "2":
            console.print("You selected Members.")
            return choice
        elif choice == "3":
            console.print("You selected Rentals.")
            return choice
        elif choice == "4":
            confirm_exit = input("Are you sure you want to exit? (y/n): ").strip().lower()
            if confirm_exit == "y":
                console.print("Exiting the program.")
                return choice
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
