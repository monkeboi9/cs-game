import pygame

class Visuals:
    def __init__(self, WINDOW_RES):
        self.WINDOW_RES = WINDOW_RES
        self.DIMENSIONS = int(input("Dimensions:"))
        self.UNIT_RES = self.WINDOW_RES // self.DIMENSIONS
        self.window = pygame.display.set_mode((self.WINDOW_RES, self.WINDOW_RES))
        self.first_layer = pygame.Surface((self.WINDOW_RES, self.WINDOW_RES), pygame.SRCALPHA)
        self.assets = Assets(self.WINDOW_RES, self.UNIT_RES)
    def draw_maze_data(self, data, direction):
        transparency = 0xE0
        BLACK = (0x0, 0x0, 0x0, transparency)
        LIGHT_GREEN = (0x90, 0xee, 0x90, transparency)
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
        self.first_layer.fill((0xFF, 0xFF, 0xFF, 0x0))
        self.window.blit(self.assets.background, self.assets.background_rect)
        self.draw_maze_data(data, direction)
        self.window.blit(self.first_layer, (0, 0))
        pygame.display.update()
class Assets:
    def __init__(self, resolution, unit):
        self.background = pygame.image.load("assets/background.jpg")
        self.background = pygame.transform.scale(self.background, (resolution, resolution))
        self.background_rect = self.background.get_rect()
        self.down = self.load_and_scale("assets/down.png", unit)
        self.up = self.load_and_scale("assets/up.png", unit)
        self.left = self.load_and_scale("assets/left.png", unit)
        self.right = self.load_and_scale("assets/right.png", unit)
    def load_and_scale(self, file, unit):
        image = pygame.image.load(file)
        image = pygame.transform.scale(image, (unit, unit))
        return image
