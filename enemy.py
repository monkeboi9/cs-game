import entity

class Enemy:
    def __init__(self, maze, amount):
        self.number = amount
        self.entities = []
        for _ in range(amount):
            self.entities.append(entity.spawn(maze, 4))
    def toggle(self, maze, state):
        toggle_to = 0
        if state:
            toggle_to = 4
        for enemy in self.entities:
            maze.data[enemy.pos] = toggle_to
