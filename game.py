import sys
from maze import Maze
from player import Player
import visuals
import pygame

class Game:
    def __init__(self):
        self.WINDOW_RESOLUTION = 1200
        self.MAZE_UNIT = self.WINDOW_RESOLUTION // int(input("dimensions of maze: "))
        self.maze = Maze(self.WINDOW_RESOLUTION // self.MAZE_UNIT)
        self.generate_level()
        pygame.init()
        self.window = pygame.display.set_mode((self.WINDOW_RESOLUTION, self.WINDOW_RESOLUTION)) 
        self.first_layer = pygame.Surface((self.WINDOW_RESOLUTION, self.WINDOW_RESOLUTION), pygame.SRCALPHA)
        self.assets = visuals.Assets(self.WINDOW_RESOLUTION, self.MAZE_UNIT)
    def update(self):
        self.check_events()
        self.first_layer.fill((255, 255, 255, 0))
        self.finished_maze()
        self.window.blit(self.assets.background, self.assets.background_rect)
        visuals.draw_maze_data(self.assets.character, self.MAZE_UNIT, self.first_layer, self.maze.data)
        self.window.blit(self.first_layer, (0, 0))
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
        new_pos = tuple(map(sum, zip(self.player.pos, change)))
        if self.maze.is_valid(new_pos):
            if self.maze.data[new_pos] != 1:
                self.player.pos = new_pos