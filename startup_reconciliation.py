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

            # if under 14 days overdue but not under 0, add $1 dollar to late fee total per day overdue and
            # block the associated member's account
            if days_overdue.days < 14 and days_overdue.days > 0:
                value["late_fees_total"] = Decimal(value["late_fees_total"]) + Decimal(days_overdue.days)
                member_id = value["membership_id"]
                data["members"][member_id]["account_status"] = "true"
            # if 14 days or more overdue, mark the rental as lost,
            # set the replacement charge to "false", and decrement the total copies of the game by 1
            else:
                value.update(
                    {
                        "replacement_charge": "false",
                        "late_fees_total": 0.0,
                        "return_status": "lost",
                    }
                )
                game_id = value["game_id"]
                data["game_records"][game_id]["total_copies"] -= 1
                member_id = value["membership_id"]
                data["members"][member_id]["account_status"] = "true"

    return data
