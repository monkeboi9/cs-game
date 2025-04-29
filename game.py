import sys
from maze import Maze
from player import Player
from visuals import Visuals
import pygame

class Game:
    def __init__(self):
        RESOLUTION = 1000
        self.visuals = Visuals(RESOLUTION)
        self.maze = Maze(RESOLUTION // self.visuals.UNIT_RES)
        self.level_number = 1
        self.generate_level()
        pygame.init()
    def update(self):
        self.check_events()
        self.finished_maze()
        self.visuals.draw(self.maze.data, self.player.direction)
    def generate_level(self):
        self.maze.generate_maze()
        self.maze.make_start_pos()
        self.maze.make_end_pos()
        self.player = Player(self.maze.start_pos)
        self.level_number += 1
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
            self.player.direction = "left"
        if key_type == pygame.K_d:
            change = (1, 0)
            self.player.direction = "right"
        if key_type == pygame.K_w:
            change = (0, -1)
            self.player.direction = "up"
        if key_type == pygame.K_s:
            change = (0, 1)
            self.player.direction = "down"
        if key_type == pygame.K_r:
            self.generate_level()
        self.maze.move_cell(self.player.pos, change)
        new_pos = tuple(map(sum, zip(self.player.pos, change)))
        if self.maze.is_valid(new_pos):
            if self.maze.data[new_pos] != 1:
                self.player.pos = new_pos
