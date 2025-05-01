import pygame
from time import sleep

class Visuals:
    def __init__(self, WINDOW_RES):
        self.WINDOW_RES = WINDOW_RES
        self.DIMENSIONS = int(input("Dimensions:"))
        self.UNIT_RES = self.WINDOW_RES // self.DIMENSIONS
        self.make_layers()
        self.assets = Assets(self.WINDOW_RES, self.UNIT_RES)
    def make_layers(self):
        self.window = pygame.display.set_mode((self.WINDOW_RES, self.WINDOW_RES))
        self.first_layer = pygame.Surface((self.WINDOW_RES, self.WINDOW_RES), pygame.SRCALPHA)
        self.splash_layer = pygame.Surface((self.WINDOW_RES, self.WINDOW_RES), pygame.SRCALPHA)
    def draw_maze_data(self, data, direction):
        transparency = 0xE0
        BLACK = (0x0, 0x0, 0x0, transparency)
        LIGHT_GREEN = (0x90, 0xee, 0x90, transparency)
        RED = (0xFF, 0x0, 0x0, transparency)
        current_x = 0
        current_y = 0
        for y in range(data.shape[1]):
            for x in range(data.shape[0]):
                # 1 represents a wall
                if data[x, y] == 1:
                    pygame.draw.rect(self.first_layer, BLACK, pygame.Rect(current_x, current_y, self.UNIT_RES, self.UNIT_RES))
                # 2 represents the player
                elif data[x, y] == 2:
                    self.draw_character(direction, (current_x, current_y))
                # 3 represents the end
                elif data[x, y] == 3:
                    pygame.draw.rect(self.first_layer, LIGHT_GREEN, pygame.Rect(current_x, current_y, self.UNIT_RES, self.UNIT_RES))
                elif data[x, y] == 4:
                    self.first_layer.blit(self.assets.worm, (current_x, current_y))
                elif data[x, y] == 5:
                    self.first_layer.blit(self.assets.key, (current_x, current_y))
                current_x += self.UNIT_RES
            current_x = 0
            current_y += self.UNIT_RES
    def draw_character(self, direction, pos):
        if direction == "down":
            self.first_layer.blit(self.assets.down, pos)
        if direction == "up":
            self.first_layer.blit(self.assets.up, pos)
        if direction == "left":
            self.first_layer.blit(self.assets.left, pos)
        if direction == "right":
            self.first_layer.blit(self.assets.right, pos)
    def draw(self, data, direction):
        self.first_layer.fill((0x0, 0x0, 0x0, 0x0))
        self.window.blit(self.assets.background, self.assets.background_rect)
        self.draw_maze_data(data, direction)
        self.window.blit(self.first_layer, (0, 0))
        pygame.display.update()
    def show_start_splash(self):
        self.splash_layer.blit(self.assets.studio_splash, self.assets.studio_splash_rect)
        self.window.blit(self.splash_layer, (0, 0))
        pygame.display.update()
        sleep(4)
        self.splash_layer.fill((0x0, 0x0, 0x0, 0x0))
class Assets:
    def __init__(self, resolution, unit):
        self.background = self.load_and_scale("assets/background.jpg", resolution)
        self.background_rect = self.background.get_rect()
        self.load_splash_screens(resolution)
        self.down = self.load_and_scale("assets/down.png", unit)
        self.up = self.load_and_scale("assets/up.png", unit)
        self.left = self.load_and_scale("assets/left.png", unit)
        self.right = self.load_and_scale("assets/right.png", unit)
        self.key = self.load_and_scale("assets/key.png", unit)
        self.worm = self.load_and_scale("assets/worm.png", unit)
    def load_splash_screens(self, resolution):
        self.studio_splash = self.load_and_scale("assets/studio.png", resolution)
        self.studio_splash_rect = self.studio_splash.get_rect()
    def load_and_scale(self, file, unit):
        image = pygame.image.load(file)
        image = pygame.transform.scale(image, (unit, unit))
        return image
