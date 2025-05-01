import random

class Entity:
    def __init__(self, pos, value):
        self.pos = pos
        self.value = value
def spawn(maze, value):
    while True:
        cord = (random.randrange(0, maze.dimensions), random.randrange(0, maze.dimensions))
        if maze.data[cord] == 0:
            maze.data[cord] = value
            break
    return Entity(cord, value)
