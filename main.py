import pygame
import visuals
import maze


WINDOW_DIMENSIONS = 1000 
UNIT = WINDOW_DIMENSIONS // int(input("dimensions of maze: "))
maze = maze.Maze(WINDOW_DIMENSIONS // UNIT)
maze.generate_maze()
maze.make_start_pos()
maze.make_end_pos()
pygame.init()
screen = pygame.display.set_mode((WINDOW_DIMENSIONS, WINDOW_DIMENSIONS))
exit = False
while not exit: 
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            exit = True
    screen.fill((255, 255, 255))
    visuals.draw_maze_data(UNIT, screen, maze.data)
    pygame.display.update() 