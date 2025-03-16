import pygame

def draw_maze_data(unit_size, screen, data):
    BLACK = (0, 0, 0)
    current_x = 0
    current_y = 0
    for y in range(data.shape[1]):
        for x in range(data.shape[0]):
            if data[x, y] == 1:
                pygame.draw.rect(screen, BLACK, pygame.Rect(current_x, current_y, unit_size, unit_size))
            current_x += unit_size
        current_x = 0
        current_y += unit_size