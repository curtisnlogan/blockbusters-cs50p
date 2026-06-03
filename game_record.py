class GameRecord:

    game_id: str
    title: str
    platform: str
    total_copies: int
    replacement_cost: float
    
    def __init__(self, game_id: str, title: str, platform: str, total_copies: int, replacement_cost: float):
        self.game_id = game_id
        self.title = title
        self.platform = platform
        self.total_copies = total_copies
        self.replacement_cost = replacement_cost