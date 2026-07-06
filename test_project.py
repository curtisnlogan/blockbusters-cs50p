from game_record import GameRecord
from membership import Membership
from rental_record import RentalRecord

import pytest

def test_GameRecord():
    GameRecord1 = GameRecord("  Hogs of War   ", "playstation_1", 10)
    assert GameRecord1.title == "hogs of war"


def test_Membership():
    Membership1 = Membership("H.P. Lovecraft", True, "   66 college Street in providence, rhode island   ", "Credit Card")
    assert Membership1.address == "66 College Street In Providence, Rhode Island"


def test_RentalRecord():
    RentalRecord1 = RentalRecord("a1a34c72-9dd2-41c3-8a79-6d06c7970b4b", "dcbc1fd1-bdd1-4435-a09f-e59e63b6b604")
    with pytest.raises(ValueError):
        RentalRecord1.membership_id = ""