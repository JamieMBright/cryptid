"""
Cryptids.

Run the Cryptids trading card game.
"""
import traceback

import pygame

from cryptids import settings
from cryptids.game import Game

# Initialize Pygame
pygame.init()

# Set window size and title
screen = pygame.display.set_mode((settings.WINWIDTH, settings.WINHEIGHT))
pygame.display.set_caption(settings.WINTITLE)

# Set up game clock
clock = pygame.time.Clock()

# initialize the game
game = Game()


def main():
    """Run Cryptids."""
    # Game loop
    running = True
    while running:
        # Handle events
        for event in pygame.event.get():

            # check if the window is closed
            if event.type == pygame.QUIT:
                # if so, end the script by breaking the while loop
                running = False

        # do stuff
        try:
            game.render(screen)
        except BaseException:
            print(traceback.format_exc())
            running = False

        # await interaction

        # Update the display
        pygame.display.update()

        # Limit frame rate to 60 FPS
        clock.tick(settings.CLOCKSPEED)

    # Quit Pygame
    pygame.quit()


if __name__ == "__main__":
    main()
