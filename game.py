import sys
from maze import Maze
from player import Player
from visuals import Visuals
from enemy import Enemy
import entity
import pygame

class Game:
    def __init__(self):
        RESOLUTION = 1000
        self.last_toggle_time = pygame.time.get_ticks()
        self.toggle_interval = 1500
        self.toggle_state = True
        self.visuals = Visuals(RESOLUTION)
        self.maze = Maze(RESOLUTION // self.visuals.UNIT_RES)
        self.level_number = 0
        self.health = 5
        self.generate_level()
        self.clock = pygame.time.Clock()
        pygame.init()
        self.visuals.show_start_splash()
    def update(self):
        self.check_events()
        self.check_keys()
        self.check_key_for_portal()
        self.finished_maze()
        self.check_toggle()
        self.check_enemies()
        self.visuals.draw(self.maze.data, self.player.direction, self.level_number, self.health)
        self.clock.tick(15)
    def check_toggle(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_toggle_time >= self.toggle_interval:
            self.toggle_state = not self.toggle_state
            self.last_toggle_time = current_time
            self.enemy.toggle(self.maze, self.toggle_state)
    def generate_level(self):
        if self.level_number > 2:
            self.you_win()
        self.maze.generate_maze()
        self.maze.make_start_pos()
        self.maze.make_end_pos()
        self.player = Player(self.maze.start_pos)
        self.enemy = Enemy(self.maze, self.maze.dimensions // 2)
        self.key = entity.spawn(self.maze, 5)
        self.level_number += 1
        self.visuals.assets.switch_bg()
    def finished_maze(self):
            if self.player.pos == self.maze.end_pos:
                if self.player.has_key:
                    self.generate_level()
                else:
                    self.kill_player()
    def check_key_for_portal(self):
        if self.player.pos == self.key.pos:
            self.player.has_key = True
    def check_enemies(self):
        if self.toggle_state:
            for enemy in self.enemy.entities:
                if self.player.pos == enemy.pos:
                    self.kill_player(enemy)
                    break
    def game_over(self):
        self.visuals.show_game_over()
        pygame.quit()
        sys.exit()
    def you_win(self):
        self.visuals.show_win_screen()
        pygame.quit()
        sys.exit()
    def kill_player(self, enemy=-1):
        self.maze.data[self.player.pos] = 0
        self.maze.data[self.maze.start_pos] = 2 
        self.player.pos = self.maze.start_pos
        if enemy != -1:
            self.enemy.entities.remove(enemy)
        if self.health == 1:
            self.game_over()
        self.health -= 1
        self.maze.make_end_pos()
    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
    def check_keys(self):
        keys = pygame.key.get_pressed()
        change = (0, 0)
        if keys[pygame.K_a]:
            change = (-1, 0)
            self.player.direction = "left"
        elif keys[pygame.K_d]:
            change = (1, 0)
            self.player.direction = "right"
        elif keys[pygame.K_w]:
            change = (0, -1)
            self.player.direction = "up"
        elif keys[pygame.K_s]:
            change = (0, 1)
            self.player.direction = "down"
        if keys[pygame.K_r]:
            self.generate_level()
        if change != (0,0):
            self.player.pos = self.maze.move_cell(self.player.pos, change)
