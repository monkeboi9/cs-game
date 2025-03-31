import pygame

def draw_maze_data(unit_size, screen, data):
    transparency = 0xE0
    BLACK = (0x0, 0x0, 0x0, transparency)
    YELLOW = (0xFF, 0xFF, 0x0, transparency)
    LIGHT_GREEN = (0x90, 0xee, 0x90, transparency)
    current_x = 0
    current_y = 0
    for y in range(data.shape[1]):
        for x in range(data.shape[0]):
            if data[x, y] == 1:
                pygame.draw.rect(screen, BLACK, pygame.Rect(current_x, current_y, unit_size, unit_size))
            elif data[x, y] == 2:
                pygame.draw.rect(screen, YELLOW, pygame.Rect(current_x, current_y, unit_size, unit_size))
            elif data[x, y] == 3:
                pygame.draw.rect(screen, LIGHT_GREEN, pygame.Rect(current_x, current_y, unit_size, unit_size))
            current_x += unit_size
        current_x = 0
        current_y += unit_size
def draw_background(resolution, screen):
    background = pygame.image.load("assets/background.jpg")
    background = pygame.transform.scale(background, (resolution, resolution))
    imagerect = background.get_rect()
    screen.blit(background, imagerect)