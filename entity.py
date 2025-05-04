import random

# Represents an object in the maze (like a key or enemy) with a position and a type value
class Entity:
    def __init__(self, pos, value):
        self.pos = pos  # (x, y) position in the maze
        self.value = value  # Identifier (e.g., 4 for enemy, 5 for key)

# Spawns an entity of a given value at a random empty location in the maze
def spawn(maze, value):
    while True:
        # Choose random coordinates within maze bounds
        cord = (random.randrange(0, maze.dimensions), random.randrange(0, maze.dimensions))
        if maze.data[cord] == 0:  # Make sure the cell is empty
            maze.data[cord] = value  # Place the entity in the maze
            break
    return Entity(cord, value)  # Return a new Entity object with its position and type
