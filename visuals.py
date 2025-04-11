import pygame

def draw_maze_data(assets, unit_size, screen, data, direction):
    transparency = 0xE0
    BLACK = (0x0, 0x0, 0x0, transparency)
    LIGHT_GREEN = (0x90, 0xee, 0x90, transparency)
    current_x = 0
    current_y = 0
    for y in range(data.shape[1]):
        for x in range(data.shape[0]):
            if data[x, y] == 1:
                pygame.draw.rect(screen, BLACK, pygame.Rect(current_x, current_y, unit_size, unit_size))
            elif data[x, y] == 2:
                draw_character(screen, assets, direction, (current_x, current_y))
            elif data[x, y] == 3:
                pygame.draw.rect(screen, LIGHT_GREEN, pygame.Rect(current_x, current_y, unit_size, unit_size))
            current_x += unit_size
        current_x = 0
        current_y += unit_size
def draw_character(screen, assets, direction, pos):
    if direction == "down":
        screen.blit(assets.down, pos)
    if direction == "up":
        screen.blit(assets.up, pos)
    if direction == "left":
        screen.blit(assets.left, pos)
    if direction == "right":
        screen.blit(assets.right, pos)
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
