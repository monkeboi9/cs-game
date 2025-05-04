import pygame
from time import sleep

# Handles all visuals: window, maze drawing, splash screens, HUD
class Visuals:
    def __init__(self, WINDOW_RES):
        self.WINDOW_RES = WINDOW_RES  # Window resolution (1000x1000)
        self.DIMENSIONS = int(input("Dimensions:"))  # Maze dimensions (20 for 20x20 grid)
        self.UNIT_RES = self.WINDOW_RES // self.DIMENSIONS  # Size of each tile in pixels
        self.make_layers()  # Initialize drawing layers
        self.assets = Assets(self.WINDOW_RES, self.UNIT_RES)  # Load images and sprites

    # Creates rendering layers: main window, maze layer, splash screen layer
    def make_layers(self):
        self.window = pygame.display.set_mode((self.WINDOW_RES, self.WINDOW_RES))
        self.first_layer = pygame.Surface((self.WINDOW_RES, self.WINDOW_RES), pygame.SRCALPHA)
        self.splash_layer = pygame.Surface((self.WINDOW_RES, self.WINDOW_RES), pygame.SRCALPHA)

    # Draws maze elements based on encoded tile values
    def draw_maze_data(self, data, direction):
        transparency = 0xE0 # Transparency so the background is more visible
        BLACK = (0x0, 0x0, 0x0, transparency)
        LIGHT_GREEN = (0x90, 0xee, 0x90, transparency)
        current_x = 0
        current_y = 0
        for y in range(data.shape[1]):
            for x in range(data.shape[0]):
                if data[x, y] == 1:  # Wall tile
                    pygame.draw.rect(self.first_layer, BLACK, pygame.Rect(current_x, current_y, self.UNIT_RES, self.UNIT_RES))
                elif data[x, y] == 2:  # Player tile
                    self.draw_character(direction, (current_x, current_y))
                elif data[x, y] == 3:  # End/goal tile
                    pygame.draw.rect(self.first_layer, LIGHT_GREEN, pygame.Rect(current_x, current_y, self.UNIT_RES, self.UNIT_RES))
                elif data[x, y] == 4:  # Enemy (worm) tile
                    self.first_layer.blit(self.assets.worm, (current_x, current_y))
                elif data[x, y] == 5:  # Key tile
                    self.first_layer.blit(self.assets.key, (current_x, current_y))
                current_x += self.UNIT_RES
            current_x = 0
            current_y += self.UNIT_RES

    # Draws player sprite in the correct direction
    def draw_character(self, direction, pos):
        if direction == "down":
            self.first_layer.blit(self.assets.down, pos)
        if direction == "up":
            self.first_layer.blit(self.assets.up, pos)
        if direction == "left":
            self.first_layer.blit(self.assets.left, pos)
        if direction == "right":
            self.first_layer.blit(self.assets.right, pos)

    # Draws everything for one frame: background, maze, player, HUD
    def draw(self, data, direction, level, lives):
        self.first_layer.fill((0x0, 0x0, 0x0, 0x0))  # Clear previous frame
        self.window.blit(self.assets.background, self.assets.background_rect)  # Draw background
        self.draw_maze_data(data, direction)  # Draw maze and characters
        self.window.blit(self.first_layer, (0, 0))  # Overlay maze on background
        self.draw_status_bar(level, lives)  # Show level and lives
        pygame.display.update()  # Update the display

    # Displays level and lives at top of screen
    def draw_status_bar(self, level, lives):
        font = pygame.font.SysFont("arial", 24, bold=True)
        text_color = (255, 255, 255)
        background_color = (0, 0, 0, 128)  # Semi-transparent black
        status_surface = pygame.Surface((self.WINDOW_RES, 30), pygame.SRCALPHA)
        status_surface.fill(background_color)
        status_text = f"Level: {level}    Lives: {lives}"
        text_surface = font.render(status_text, True, text_color)
        status_surface.blit(text_surface, (10, 5))  # Draw text
        self.window.blit(status_surface, (0, 0))  # Display on screen

    # Show the opening splash screens (studio and game logos)
    def show_start_splash(self):
        studio_splash = pygame.image.load("assets/studio.png")
        studio_splash_rect = studio_splash.get_rect()
        self.splash_layer.blit(studio_splash, studio_splash_rect)
        self.window.blit(self.splash_layer, (0, 0))
        pygame.display.update()
        sleep(2)

        game_splash = pygame.image.load("assets/game.png")
        game_splash_rect = game_splash.get_rect()
        self.splash_layer.blit(game_splash, game_splash_rect)
        self.window.blit(self.splash_layer, (0, 0))
        pygame.display.update()
        sleep(2)

    # Show the game over screen
    def show_game_over(self):
        death_splash = pygame.image.load("assets/death.png")
        death_splash_rect = death_splash.get_rect()
        self.splash_layer.blit(death_splash, death_splash_rect)
        self.window.blit(self.splash_layer, (0, 0))
        pygame.display.update()
        sleep(3)

    # Show the win screen
    def show_win_screen(self):
        win_splash = pygame.image.load("assets/win.png")
        win_splash_rect = win_splash.get_rect()
        self.splash_layer.blit(win_splash, win_splash_rect)
        self.window.blit(self.splash_layer, (0, 0))
        pygame.display.update()
        sleep(3)

# Handles loading and switching all images used in the game
class Assets:
    def __init__(self, resolution, unit):
        self.resolution = resolution  # Window resolution
        self.unit = unit  # Size of each tile in pixels

        # Load and store all background images
        self.background_images = [
            self.load_and_scale_bg("assets/table.png"),
            self.load_and_scale_bg("assets/farm.png"),
            self.load_and_scale_bg("assets/kitchen.png"),
        ]
        self.background_index = 0  # Start with the first background
        self.background = self.background_images[self.background_index]
        self.background_rect = self.background.get_rect()

        # Load and scale sprites for player and game items
        self.down = self.load_and_scale("assets/down.png", unit)
        self.up = self.load_and_scale("assets/up.png", unit)
        self.left = self.load_and_scale("assets/left.png", unit)
        self.right = self.load_and_scale("assets/right.png", unit)
        self.key = self.load_and_scale("assets/key.png", unit)
        self.worm = self.load_and_scale("assets/worm.png", unit)

    # Load and scale a sprite (for characters or items)
    def load_and_scale(self, file, unit):
        image = pygame.image.load(file)
        return pygame.transform.scale(image, (unit, unit))

    # Load and scale a background image to fit the screen
    def load_and_scale_bg(self, file):
        image = pygame.image.load(file)
        return pygame.transform.scale(image, (self.resolution, self.resolution))

    # Switch to the next background image (cycles through the list)
    def switch_bg(self):
        self.background_index = (self.background_index + 1) % len(self.background_images)
        self.background = self.background_images[self.background_index]
        self.background_rect = self.background.get_rect()
