from datetime import date
from decimal import Decimal


def reconcile(data: dict, today: date = date.today(), target: str = "rentals") -> dict:
    """
    Perform startup reconciliation on the the in-memory data dictionary in project.py.
    This function checks 'rented' games for late fees and replacement fees, and updates the data accordingly.
    It returns the reconciled data dictionary.
    """

    for value in data[target].values():
        # check if the rental status is 'rented' to determine if its a valid target for reconciliation
        if value["return_status"] == "rented":
            # convert from str to date obj for comparison
            due_date_obj = date.fromisoformat(value["due_for_return"])

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
