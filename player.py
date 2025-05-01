class Player:
    def __init__(self, start_position):
        self.direction = "down"
        self.apples = 0
        self.hearts = 5
        self.has_key = False
        self.pos = start_position
