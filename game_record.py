class GameRecord:

    __game_id: str
    __title: str
    __platform: str
    __total_copies: int
    # fixed replacement cost to $40.00 as per the requirements
    REPLACEMENT_COST: float = 40.00
    # stops the use of abbreviations for platforms and ensures that only valid platforms are used
    VALID_PLATFORMS = ["xbox", "playstation_1", "playstation_2", "n64", "nintendo_gamecube"]

    def __init__(self, game_id: str, title: str, platform: str, total_copies: int, replacement_cost: float):
        self.__game_id = game_id
        self.__title = title
        self.__platform = platform
        self.__total_copies = total_copies
        self.__replacement_cost = replacement_cost
    
    # does not have setter method as this value should not be changed after the game record is created
    @property
    def game_id(self):
        return self.__game_id
    
    @property
    def title(self):
        return self.__title
    
    @title.setter
    def title(self, new_title: str):
        if new_title is not None and new_title != "":
           self.__title = new_title.strip().lower()
        else:
            raise ValueError("Title cannot be 'None' or an empty string")

    @property
    def platform(self):
        return self.__platform
    
    @platform.setter
    def platform(self, new_platform: str):
        if new_platform is not None and new_platform != "" and new_platform in GameRecord.VALID_PLATFORMS:
            self.__platform = new_platform.strip().lower()
        else:
            raise ValueError("Platform cannot be 'None', an empty string or an invalid platform")

    @property
    def total_copies(self):
        return self.__total_copies
    
    @total_copies.setter
    def total_copies(self, new_total_copies: int):
        if isinstance(new_total_copies, int) and 0 <= new_total_copies < 100:
            self.__total_copies = new_total_copies
        else:
            raise ValueError("Total copies must be between 0 and 99 inclusive")
    # does not have setter method as this value should not be changed on a per game basis
    @property
    def replacement_cost(self):
        return self.__replacement_cost
    