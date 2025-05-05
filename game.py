# Import required modules
import sys
from maze import Maze
from player import Player
from visuals import Visuals
from enemy import Enemy
import entity
import pygame

class Game:
    def __init__(self):
        # Set screen resolution
        RESOLUTION = 1000
        # Setup for toggling enemies on/off
        self.last_toggle_time = pygame.time.get_ticks()
        self.toggle_interval = 1500  # milliseconds
        self.toggle_state = True  # Enemies start active
        # Create visuals and maze
        self.visuals = Visuals(RESOLUTION)
        self.maze = Maze(RESOLUTION // self.visuals.UNIT_RES)
        # Initial game state
        self.level_number = 0
        self.health = 5
        self.generate_level()  # Create the first level
        self.clock = pygame.time.Clock()
        pygame.init()
        self.visuals.show_start_splash()  # Show splash screen at start
        # Loads and plays music
        pygame.mixer.init()
        pygame.mixer.music.load("assets/music.wav")
        pygame.mixer.music.set_volume(0.7)
        pygame.mixer.music.play(-1)
    def update(self):
        # Called every frame to update the game
        self.check_events()
        self.check_keys()
        self.check_key_for_portal()
        self.finished_maze()
        self.check_toggle()
        self.check_enemies()
        # Draw the updated game screen
        self.visuals.draw(self.maze.data, self.player.direction, self.level_number, self.health)
        self.clock.tick(15)  # Limit to 15 frames per second

    def check_toggle(self):
        # Toggle enemy behavior every few seconds
        current_time = pygame.time.get_ticks()
        if current_time - self.last_toggle_time >= self.toggle_interval:
            self.toggle_state = not self.toggle_state
            self.last_toggle_time = current_time
            self.enemy.toggle(self.maze, self.toggle_state)

    def generate_level(self):
        # Move to next level or end game if all levels complete
        if self.level_number > 2:
            self.you_win()
        self.maze.generate_maze()
        self.maze.make_start_pos()
        self.maze.make_end_pos()
        self.player = Player(self.maze.start_pos)
        self.enemy = Enemy(self.maze, self.maze.dimensions // 2)
        self.key = entity.spawn(self.maze, 5)  # Place a key in the maze
        self.level_number += 1
        self.visuals.assets.switch_bg()  # Change background visuals

    def finished_maze(self):
        # Check if player has reached the exit
        if self.player.pos == self.maze.end_pos:
            if self.player.has_key:
                self.generate_level()  # Go to next level
            else:
                self.kill_player()  # Player dies if no key

    def check_key_for_portal(self):
        # Check if player picked up the key
        if self.player.pos == self.key.pos and not self.player.has_key:
            self.player.has_key = True
            sound = pygame.mixer.Sound("assets/key.mp3")
            sound.play()

    def check_enemies(self):
        # Check for collision with active enemies
        if self.toggle_state:
            for enemy in self.enemy.entities:
                if self.player.pos == enemy.pos:
                    self.kill_player(enemy)
                    break

    def game_over(self):
        # End the game and quit
        pygame.mixer.music.pause()
        sound = pygame.mixer.Sound("assets/death.wav")
        sound.play()
        self.visuals.show_game_over()
        pygame.quit()
        sys.exit()

    def you_win(self):
        # Player won the game
        sound = pygame.mixer.Sound("assets/yay.mp3")
        sound.play()
        self.visuals.show_win_screen()
        pygame.quit()
        sys.exit()

    def kill_player(self, enemy=-1):
        # Reset player position and update health on death
        sound = pygame.mixer.Sound("assets/damage.mp3")
        sound.play()
        self.maze.data[self.player.pos] = 0  # Clear player position
        self.maze.data[self.maze.start_pos] = 2  # Mark start position
        self.player.pos = self.maze.start_pos  # Move player to start
        if enemy != -1:
            self.enemy.entities.remove(enemy)  # Remove enemy if killed player
        if self.health == 1:
            self.game_over()
        self.health -= 1
        self.maze.make_end_pos()  # Move portal to new position

    def check_events(self):
        # Handle game window events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def check_keys(self):
        # Handle player movement and level reset
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
            self.generate_level()  # Restart the current level
        if change != (0, 0):
            # Move player if a movement key was pressed
            self.player.pos = self.maze.move_cell(self.player.pos, change)
