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
    def is_over_18(self):
        return self.__is_over_18
    
    @is_over_18.setter
    def is_over_18(self, new_is_over_18):
        if new_is_over_18 is True or new_is_over_18 is False:
            self.__is_over_18 = new_is_over_18
        else:
            raise ValueError("Over 18 check must be either 'True' or 'False'.")

    @property
    def address(self):
        return self.__address

    @address.setter
    def address(self, new_address):
        if new_address is not None or new_address != "":
            self.__address = new_address.strip().title()
        else:
            raise ValueError("Address cannot be 'None' or an empty string.")

    @property
    def payment_method(self):
        return self.__payment_method

    @payment_method.setter
    def payment_method(self, new_payment_method):
        if new_payment_method in Membership.PAYMENT_METHOD:
            self.__payment_method = new_payment_method.strip().title()
        else:
            raise ValueError(
                "Invalid payment method. Enter either 'Debit Card' or 'Credit Card'."
            )

    @property
    def account_status(self):
        return self.__account_status
    
    @account_status.setter
    def account_status(self, new_account_status):
        if new_account_status is True or new_account_status is False:
            self.__account_status = new_account_status
        else:
            raise ValueError(
                "Account status must be either 'True' (active) or 'False' (blocked)."
            )
