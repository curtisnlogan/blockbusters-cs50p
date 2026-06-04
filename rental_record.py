"""
##### rental logs

- `rental_id` - id: auto generated
- `membership_id` - from membership accounts
- `game_id` - from game inventory
- `date_rented` - always current date
- `due_for_return` - always 7 days after rented date
- `late_fees_total` - default: $0
- `replacement_charge` - default: false
- `return_status` - default: rented
"""

from datetime import date, timedelta
from uuid import uuid4
from typing import Union


class RentalRecord:
    RETURN_STATUS = ["rented", "returned", "lost"]

    def __init__(
        self,
        membership_id: Union[str, int],
        game_id: Union[str, int],
    ):
        self.__rental_id = str(uuid4())
        self.membership_id = membership_id
        self.game_id = game_id
        self.__date_rented = date.today()
        self.__due_for_return = self.__date_rented + timedelta(days=7)
        # not ideal for product code (floating point precision), 
        # but for the sake of simplicity, we will use a float to represent the total late fees.
        self.late_fees_total = 0.0
        self.replacement_charge = False
        self.return_status = "rented"

    def __str__(self):
        return (
            f"RentalRecord:\n"
            f"  rental_id={self.__rental_id}\n"
            f"  membership_id={self.membership_id}\n"
            f"  game_id={self.game_id}\n"
            f"  date_rented={self.__date_rented}\n"
            f"  due_for_return={self.__due_for_return}\n"
            f"  late_fees_total={self.late_fees_total}\n"
            f"  replacement_charge={self.replacement_charge}\n"
            f"  return_status={self.return_status}\n"
        )

    @property
    def rental_id(self):
        return self.__rental_id

    @property
    def membership_id(self):
        return self.__membership_id

    @membership_id.setter
    def membership_id(self, new_membership_id: Union[str, int]):
        if isinstance(new_membership_id, (str, int)) and new_membership_id != "":
            self.__membership_id = (
                new_membership_id.strip()
                if isinstance(new_membership_id, str)
                else new_membership_id
            )
        else:
            raise ValueError(
                "Memebership ID must be either a str or int and not an empty string."
            )

    @property
    def game_id(self):
        return self.__game_id

    @game_id.setter
    def game_id(self, new_game_id: Union[str, int]):
        if isinstance(new_game_id, (str, int)) and new_game_id != "":
            self.__game_id = (
                new_game_id.strip() if isinstance(new_game_id, str) else new_game_id
            )
        else:
            raise ValueError(
                "Game ID must be either a str or int and not an empty string."
            )
    
    @property
    def date_rented(self):
        return self.__date_rented
    
    @property
    def due_for_return(self):
        return self.__due_for_return
    
    @property
    def late_fees_total(self):
        return self.__late_fees_total
    
    @late_fees_total.setter
    def late_fees_total(self, new_late_fees_total: float):
        if isinstance(new_late_fees_total, float) and new_late_fees_total >= 0.0:
            self.__late_fees_total = new_late_fees_total
        else:
            raise ValueError("Late fees total must be a non-negative float.")
        
    @property
    def replacement_charge(self):
        return self.__replacement_charge
    
    @replacement_charge.setter
    def replacement_charge(self, new_replacement_charge: bool):
        if new_replacement_charge is True or new_replacement_charge is False:
            self.__replacement_charge = new_replacement_charge
        else:
            raise ValueError(
                "Replacement charge must be a boolean value (True or False)."
            )
    
    @property
    def return_status(self):
        return self.__return_status
    
    @return_status.setter
    def return_status(self, new_return_status: str):
        if new_return_status in RentalRecord.RETURN_STATUS:
            self.__return_status = new_return_status
        else:
            raise ValueError(
                f"Return status must be one of the following: {', '.join(self.RETURN_STATUS)}."
            )