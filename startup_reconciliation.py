from datetime import date
from decimal import Decimal


def reconcile(data: dict, target: str, today: date) -> dict:
    """
    Perform startup reconciliation on the the in-memory data dictionary in project.py.
    This function checks 'rented' games for late fees and replacement fees, and updates the data accordingly.
    It returns the reconciled data dictionary.
    """

    # dict comprhensions for 0(1) lookups of members and games by their IDs
    members_by_id = {member["member_id"]: member for member in data["members"]}
    games_by_id = {game["game_id"]: game for game in data["game_records"]}

    for record, details in data[target].items():
            # check if the rental status is 'rented' to determine if we need to perform reconciliation
            if record["rental_status"] == "rented":

                # convert from str to date obj for comparison
                due_date_obj = date.fromisoformat(record["due_for_return"])

            # get timedelta for diff between both dates
            days_overdue = today - due_date_obj

                # if under 14 days overdue, add $1 dollar to late fee total per day overdue and 
                # block the associated member's account
                if days_overdue.days < 14:
                     record["late_fees_total"] = 0
                     record["late_fees_total"] += days_overdue.days
                     # block associated member's account
                     members_by_id[record["member_id"]]["account_blocked"] = True
                # if 14 days or more overdue, mark the rental as lost, 
                # set the replacement charge to False, and decrement the total copies of the game by 1
                else:
                     record.update({"replacement_charge": False, "late_fees_total": 0, "return_status": "lost"})
                     game_id = record["game_id"]
                     games_by_id[game_id]["total_copies"] -= 1
                     members_by_id[record["member_id"]]["account_blocked"] = True

    return data
