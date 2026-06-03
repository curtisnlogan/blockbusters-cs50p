class GameRecord:

    __game_id: str
    __title: str
    __platform: str
    __total_copies: int
    __replacement_cost: float

    def __init__(self, game_id: str, title: str, platform: str, total_copies: int, replacement_cost: float):
        self.__game_id = game_id
        self.__title = title
        self.__platform = platform
        self.__total_copies = total_copies
        self.__replacement_cost = replacement_cost
    
    def game_id(self):
        return self.__game_id
    
    def title(self):
        return self.__title
    
    def platform(self):
        return self.__platform
    
    def total_copies(self):
        return self.__total_copies
    
    def replacement_cost(self):
        return self.__replacement_cost