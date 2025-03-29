import sys
from maze import Maze
from player import Player
import visuals
import pygame

class Game:
    def __init__(self):
        self.WINDOW_RESOLUTION = 1000
        self.MAZE_UNIT = self.WINDOW_RESOLUTION // int(input("dimensions of maze: "))
        self.maze = Maze(self.WINDOW_RESOLUTION // self.MAZE_UNIT)
        self.generate_level()
        print("start:", self.player.pos)
        pygame.init()
        self.screen = pygame.display.set_mode((self.WINDOW_RESOLUTION, self.WINDOW_RESOLUTION)) 
    def update(self):
        self.check_events()
        self.screen.fill((255, 255, 255))
        self.finished_maze()
        visuals.draw_maze_data(self.MAZE_UNIT, self.screen, self.maze.data)
        pygame.display.update()
    def generate_level(self):
        self.maze.generate_maze()
        self.maze.make_start_pos()
        self.maze.make_end_pos()
        self.player = Player(self.maze.start_pos)
    def finished_maze(self):
        if self.player.pos == self.maze.end_pos:
            self.generate_level()
    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                self.check_keys(event.key)
    def check_keys(self, key_type):
        change = (0, 0)
        if key_type == pygame.K_a:
            change = (-1, 0)
        if key_type == pygame.K_d:
            change = (1, 0)
        if key_type == pygame.K_w:
            change = (0, -1)
        if key_type == pygame.K_s:
            change = (0, 1)
        self.maze.move_cell(self.player.pos, change)
        print("player:", self.player.pos)
        new_pos = tuple(map(sum, zip(self.player.pos, change)))
        if self.maze.is_valid(new_pos):
            if self.maze.data[new_pos] != 1:
                self.player.pos = new_pos
    def next_level(self):
        pass