import numpy as np
import random

class Maze:
    def __init__(self, dimensions):
        self.data = np.ones((dimensions, dimensions), dtype=int)
        self.dimensions = dimensions
        self.frontiers = []

    def calculate_frontiers(self, x: int, y: int):
        frontiers = self.two_away(x, y, 1)
        self.frontiers.extend(frontiers)

    def two_away(self, x: int, y: int, number: int):
        output = []
        directions = [(2, 0), (-2, 0), (0, 2), (0, -2)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.dimensions and 0 <= ny < self.dimensions and self.data[nx, ny] == number:
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
            self.data[cell_between[0], cell_between[1]] = 0
            self.data[selected_frontier[0], selected_frontier[1]] = 0
            self.calculate_frontiers(selected_frontier[0], selected_frontier[1])
            self.frontiers = list(set(self.frontiers))

    def generate_maze(self):
        random_x = random.randrange(0, self.dimensions)
        random_y = random.randrange(0, self.dimensions)
        self.data[random_x, random_y] = 0
        self.calculate_frontiers(random_x, random_y)
        while self.frontiers:
            self.create_path()