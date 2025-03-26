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
            
    def make_start_pos(self):
        possible_cords = [(0, 0), (0, 1), (1, 0), (1, 1)]
        for i in possible_cords:
            if self.data[i[0], i[1]] == 0:
                self.data[i[0], i[1]] = 2
                return [i[0], i[1]]
    def make_end_pos(self):
        edge = self.dimensions - 1
        inner = edge - 1
        possible_cords = [(edge, edge), (edge, inner), (inner, inner), (inner, edge)]
        for i in possible_cords:
            if self.data[i[0], i[1]] == 0:
                self.data[i[0], i[1]] = 3
                return [i[0], i[1]]