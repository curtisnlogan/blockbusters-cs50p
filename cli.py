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
    console.print(
        "\nWelcome to the Blockbusters CLI! All data has been successfully loaded into memory."
        "Please select an option from the menu below:"
    )
    console.print("\nMain Menu:")
    console.print("1. Game Records")
    console.print("2. Members")
    console.print("3. Rentals")
    console.print("4. Exit")

    choice = input("Enter your choice (1-4): ")
    if choice not in ["1", "2", "3", "4"]:
        raise ValueError("Invalid choice. Please enter a number precisely between 1 and 4.")
    elif choice == 2:
        print("You selected Members. This feature is not yet implemented.")
        return choice
    elif choice == 3:
        print("You selected Rentals. This feature is not yet implemented.")
        return choice
    elif choice == 4:
        print("Exiting the program. Goodbye!")
        return choice

def view_game_records(game_records):

    # create a table to display game records
    table = Table(title="Game Records")

    #define columns
    table.add_column("Game ID", justify="right")
    table.add_column("Title", justify="right")
    table.add_column("Platform", justify="right")
    table.add_column("Total Copies", justify="right")
    table.add_column("Replacement Cost", justify="right")

    #build rows
    for game in game_records:
        table.add_row(game_records["game_id"], game_records["title"], game_records["platform"], 
                      str(game_records["total_copies"]), str(game_records["replacement_cost"]))

    #end
    console.print(table)