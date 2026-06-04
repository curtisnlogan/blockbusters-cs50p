"""
- `membership_id` - id: auto generated
- `full_name`
- `date_of_birth` - format: DD/MM/YY
- `address`
- `payment_method`
- `account_status` - default: active
"""

from uuid import uuid4


class Membership:
    PAYMENT_METHOD = ["Debit Card", "Credit Card"]

    def __init__(
        self, full_name: str, is_over_18: bool, address: str, payment_method: str
    ):
        self.__membership_id = str(uuid4())  # Auto-generated unique ID
        self.full_name = full_name
        self.is_over_18 = is_over_18
        self.address = address
        self.payment_method = payment_method
        self.__account_status = True  # Default: active

    def __str__(self):
        return (
            f"Membership ID: {self.__membership_id}\n"
            f"Full Name: {self.full_name}\n"
            f"Is Over 18: {'Yes' if self.is_over_18 is True else 'No'}\n"
            f"Address: {self.address}\n"
            f"Payment Method: {self.payment_method}\n"
            f"Account Status: {'Active' if self.__account_status else 'Blocked'}"
        )

    @property
    def full_name(self):
        return self.__full_name

    @full_name.setter
    def full_name(self, new_full_name: str):
        if new_full_name is not None and new_full_name != "":
            self.__full_name = new_full_name.strip().title()
        else:
            raise ValueError("A name cannot be 'None' or an empty string.")

    @property
    def date_of_birth(self):
        return self.__date_of_birth

    @date_of_birth.setter
    def date_of_birth(self, new_date_of_birth: str): 
        raise NotImplementedError("Date of birth validation is not implemented yet.")
