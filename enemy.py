from entity import Entity
import random

class Enemy:
    def __init__(self, maze, amount):
        self.number = amount
        self.entities = []
        for enemy in range(amount):
            self.spawn_random(maze)
    def spawn_random(self, maze):
        while True:
            cord = (random.randrange(0, maze.dimensions), random.randrange(0, maze.dimensions))
            if maze.data[cord] == 0:
                self.entities.append(Entity(cord, 4))            
                maze.data[cord] = 4
                break
    def toggle(self, maze, state):
        toggle_to = 0
        if state:
            toggle_to = 4
        for enemy in self.entities:
            maze.data[enemy.pos] = toggle_to
