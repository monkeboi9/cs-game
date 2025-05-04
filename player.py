# Represents the player character in the game
class Player:
    def __init__(self, start_position):
        self.direction = "down"       # Initial facing direction of the player
        self.has_key = False          # Tracks whether the player has collected the key
        self.pos = start_position     # Current position of the player on the maze grid
