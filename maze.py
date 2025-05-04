
import numpy as np
import random

# This class is a 2d numpy array that represents the maze.
# The data in this includes which coordinates are the player, empty space, wall, enemy, etc.
# This maze is randomly generated using a modified version of Prim's algorithm.
# Link to description of algorithm: https://en.wikipedia.org/wiki/Maze_generation_algorithm#Iterative_randomized_Prim's_algorithm_(without_stack,_without_sets)
class Maze:
    def __init__(self, dimensions):
        # Starts off by creating a square 2d numpy array full of ones.
        # This array is dimensions^2 so it matches up with the frontend.
        self.data = np.ones((dimensions, dimensions), dtype=int)
        self.dimensions = dimensions
        # The start pos are the coordinates where the player will spawn.
        # (0, 0) is a placeholder value because the maze might generate over it.
        self.start_pos = (0, 0)
        # Another placeholder value for the end pos
        self.end_pos = [dimensions - 1, dimensions - 1]
        self.frontiers = []  # Stores frontiers that will be explored

    # This function adds the frontiers that are two units away from the given x, y position.
    def calculate_frontiers(self, x: int, y: int):
        frontiers = self.two_away(x, y, 1)  # Get frontiers 2 units away that are walls (1)
        self.frontiers.extend(frontiers)  # Add them to the list of frontiers

    # Finds coordinates that are two units away from the current (x, y) and are walls (value = 1)
    def two_away(self, x: int, y: int, number: int):
        output = []  # List to hold frontiers
        directions = [(2, 0), (-2, 0), (0, 2), (0, -2)]  # Possible directions (2 steps)
        for dx, dy in directions:
            nx, ny = x + dx, y + dy  # New coordinates
            if self.is_valid((nx, ny)) and self.data[nx, ny] == number:  # Check if valid and wall
                output.append((nx, ny))  # Add to output if valid
        return output

    # Creates a path between the current frontier and a connected cell
    def create_path(self):
        if not self.frontiers:
            return  # If no frontiers to explore, exit
        selected_frontier = random.choice(self.frontiers)  # Select random frontier to explore
        self.frontiers.remove(selected_frontier)  # Remove frontier from list
        connecting_cells = self.two_away(selected_frontier[0], selected_frontier[1], 0)  # Find connected cells
        if connecting_cells:
            connecting_cell = random.choice(connecting_cells)  # Choose a random connected cell
            cell_between = ((selected_frontier[0] + connecting_cell[0]) // 2, 
                            (selected_frontier[1] + connecting_cell[1]) // 2)  # Midpoint between selected frontier and connecting cell
            self.data[cell_between] = 0  # Mark the cell between as a path
            self.data[selected_frontier] = 0  # Mark the selected frontier as a path
            self.calculate_frontiers(selected_frontier[0], selected_frontier[1])  # Add new frontiers
            self.frontiers = list(set(self.frontiers))  # Remove duplicates in frontiers

    # Generates the maze by adding paths using the algorithm
    def generate_maze(self):
        self.data = np.ones((self.dimensions, self.dimensions), dtype=int)  # Reset the maze
        random_x = random.randrange(0, self.dimensions)  # Random starting x
        random_y = random.randrange(0, self.dimensions)  # Random starting y
        self.data[random_x, random_y] = 0  # Mark the start position as empty
        self.calculate_frontiers(random_x, random_y)  # Calculate the frontiers
        while self.frontiers:
            self.create_path()  # Create a path while there are frontiers to explore

    # This function sets the start position of the player in the maze
    def make_start_pos(self):
        possible_cords = [(0, 0), (0, 1), (1, 0), (1, 1)]  # Possible positions near the top-left corner
        for i in possible_cords:
            if self.data[i] == 0:  # If the cell is empty
                self.data[i] = 2  # Mark it as the start position (2 represents the player)
                self.start_pos = i  # Update start position
                return i  # Return the coordinates of the start position

    # This function calculates the four possible end positions in the bottom-left corner and sets end_pos to it.
    def make_end_pos(self):
        edge = self.dimensions - 1  # The edge of the maze
        inner = edge - 1  # Inner position next to the edge
        possible_cords = [(edge, edge), (edge, inner), (inner, inner), (inner, edge)]  # Possible end positions
        for i in possible_cords:
            if self.data[i] == 0:  # If the cell is empty
                self.data[i] = 3  # Mark it as the end position (3 represents the goal)
                self.end_pos = i  # Update the end position
                return i  # Return the coordinates of the end position

    # This function moves a cell (like the player) by a given change (dx, dy)
    def move_cell(self, cord, change):
        if self.is_valid(cord, change):  # Check if the new position is valid
            new_cord = tuple(map(sum, zip(cord, change)))  # Calculate the new position
            if self.data[new_cord] != 1:  # If the new cell is not a wall
                self.data[new_cord] = self.data[cord]  # Move the cell to the new position
                self.data[cord] = 0  # Mark the old position as empty
                return new_cord  # Return the new position
        return cord  # Return the original position if move is not possible

    # This function checks whether or not a coordinate is valid to prevent an array out of bounds error.
    def is_valid(self, cord, change = (0, 0)):
        # Adds the coordinate and the change variable together to produce the new coordinate.
        # For example, cord could be the current position and change could be the direction it is going towards.
        new_cord = tuple(map(sum, zip(cord, change)))  # Calculate new coordinates
        # Checks if the x and y of the new cord are within bounds of the maze dimensions.
        if new_cord[0] > -1 and new_cord[0] < self.dimensions and new_cord[1] > -1 and new_cord[1] < self.dimensions:
            return True  # Return true if valid
        else:
            return False  # Return false if out of bounds
