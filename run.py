"""
Cryptids.

Run the Cryptids trading card game.
"""
import sys
import traceback

import pygame

from cryptids import settings
from cryptids.eventloopwrapper import GameWrapper

# Initialize Pygame
pygame.init()

# Set window size and title
screen = pygame.display.set_mode((settings.WINWIDTH, settings.WINHEIGHT))
pygame.display.set_caption(settings.WINTITLE)

# Set up game clock
clock = pygame.time.Clock()

# initialize the game
game = GameWrapper()


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
                # Quit Pygame
                pygame.quit()
                sys.exit()

            # check if a click event occured
            if event.type == pygame.MOUSEBUTTONDOWN:
                click_pos = event.pos
                print(click_pos)
            else:
                click_pos = None

            # check if any buttons were pressed
            if event.type == pygame.KEYDOWN:
                key_press = event.key
            else:
                key_press = None

        # update display
        try:
            game.render(screen, click_pos, key_press)

        except SystemExit:
            sys.exit()

        except BaseException:
            print(traceback.format_exc())
            running = False
            pygame.quit()
            sys.exit()

        # Update the display
        pygame.display.update()

        # Limit frame rate to set FPS
        clock.tick(settings.CLOCKSPEED)


if __name__ == "__main__":
    main()
