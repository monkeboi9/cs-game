import numpy as np
import random

# This class is a 2d numpy array that represents the maze.
# The data in this includes which coordinates are the player, empty space, wall, enemie, etc.
# This maze is randomly generated using a modified version of prims algorithm
# Link to description of algorithm: https://en.wikipedia.org/wiki/Maze_generation_algorithm#Iterative_randomized_Prim's_algorithm_(without_stack,_without_sets)
class Maze:
    def __init__(self, dimensions):
        # Starts off by creating a square 2d numpy array full of ones.
        # This array is dimensions^2 so it matches up with the frontend.
        self.data = np.ones((dimensions, dimensions), dtype=int)
        self.dimensions = dimensions
        # The start pos are the coordinates were the player will spawn.
        # (0, 0) is a placeholder value because the maze might generate over it.
        self.start_pos = (0, 0)
        # Another placeholder value for the end pos
        self.end_pos = (dimensions - 1, dimensions - 1)
        self.frontiers = []
    def calculate_frontiers(self, x: int, y: int):
        frontiers = self.two_away(x, y, 1)
        self.frontiers.extend(frontiers)
    def two_away(self, x: int, y: int, number: int):
        output = []
        directions = [(2, 0), (-2, 0), (0, 2), (0, -2)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if self.is_valid((nx, ny)) and self.data[nx, ny] == number:
                output.append((nx, ny))
        return output
    def create_path(self):
        if not self.frontiers:
            return
        selected_frontier = random.choice(self.frontiers)
        self.frontiers.remove(selected_frontier)
        connecting_cells = self.two_away(selected_frontier[0], selected_frontier[1], 0)
        if connecting_cells:
            connecting_cell = random.choice(connecting_cells)
            cell_between = ((selected_frontier[0] + connecting_cell[0]) // 2, (selected_frontier[1] + connecting_cell[1]) // 2)
            self.data[cell_between] = 0
            self.data[selected_frontier] = 0
            self.calculate_frontiers(selected_frontier[0], selected_frontier[1])
            self.frontiers = list(set(self.frontiers))
    def generate_maze(self):
        self.data = np.ones((self.dimensions, self.dimensions), dtype=int)
        random_x = random.randrange(0, self.dimensions)
        random_y = random.randrange(0, self.dimensions)
        self.data[random_x, random_y] = 0
        self.calculate_frontiers(random_x, random_y)
        while self.frontiers:
            self.create_path()
    def make_start_pos(self):
        possible_cords = [(0, 0), (0, 1), (1, 0), (1, 1)]
        for i in possible_cords:
            if self.data[i] == 0:
                self.data[i] = 2
                self.start_pos = i
                return i
    # This function calculates the four possible end positions in the bottom left corner and sets end_pos to it.
    def make_end_pos(self):
        edge = self.dimensions - 1
        inner = edge - 1
        possible_cords = [(edge, edge), (edge, inner), (inner, inner), (inner, edge)]
        for i in possible_cords:
            if self.data[i] == 0:
                self.data[i] = 3
                self.end_pos = i
                return i
    def move_cell(self, cord, change):
        if self.is_valid(cord, change):
            new_cord = tuple(map(sum, zip(cord, change)))
            if self.data[new_cord] != 1:
                self.data[new_cord] = self.data[cord]
                self.data[cord] = 0
                print(self.data[new_cord])
                return new_cord
        return cord
    # This function checks whether or not a coordinate is inbounds to prevent an array out of bounds error.
    def is_valid(self, cord, change = (0, 0)):
        # Adds the coordinate and the change variable together to produce the new coordinate.
        # For example, cord could be the current position and change could be the direction it is going towards.
        new_cord = tuple(map(sum, zip(cord, change)))
        # Checks if the x and y of the new cord is inbounds using greater than and less than operators.
        if new_cord[0] > -1 and new_cord[0] < self.dimensions and new_cord[1] > -1 and new_cord[1] < self.dimensions:
            # Returns true if the coordinate is not out of bounds;
            return True
        else:
            # Returns false if it is out of bounds.
            return False
