from game import Game # Imports game class from the game file

game = Game() # Creates an instance of the game class, which creates things like the window and starts splash screens
# Indefinitely call the game.update() method which manages things like frames and player movement
while True:
    game.update()
