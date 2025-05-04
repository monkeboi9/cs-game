import entity

# Manages enemy (worm) entities in the game
class Enemy:
    def __init__(self, maze, amount):
        self.number = amount  # Total number of enemies to create
        self.entities = []  # List to store enemy objects
        for _ in range(amount):
            # Spawn each enemy into the maze at a random position with value 4 (worm)
            self.entities.append(entity.spawn(maze, 4))

    # Toggles visibility of enemies on the maze grid
    def toggle(self, maze, state):
        toggle_to = 0  # If state is False, enemies disappear (value becomes 0)
        if state:
            toggle_to = 4  # If state is True, enemies appear (value is 4)
        for enemy in self.entities:
            # Update each enemy's position in the maze with the toggle value
            maze.data[enemy.pos] = toggle_to
