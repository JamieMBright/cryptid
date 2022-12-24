"""
Cryptids.

Run the Cryptids trading card game.
"""
import logging
import sys
import traceback

import pygame

from cryptids import settings
from cryptids.game import GameWrapper
from cryptids.loggingdecorator import build_logger
from cryptids.keyboard import key_interpreter

# build the game logger
logger = build_logger(logging_level=logging.DEBUG)

# Initialize Pygame
pygame.init()
logger.info("Game initialised")

# Set window size and title
screen = pygame.display.set_mode((settings.WINWIDTH, settings.WINHEIGHT))
logger.info(f"Screen size set to {(settings.WINWIDTH, settings.WINHEIGHT)}")

# set the caption
pygame.display.set_caption(settings.WINTITLE)
logger.info(f"Screen size set to {settings.WINTITLE}")

# Set up game clock
clock = pygame.time.Clock()


def main():
    """Run Cryptids."""
    # initialize the game
    logger.info("Initialising the game class: GameWrapper.")
    game = GameWrapper()

    # Game event loop
    running = True
    logger.info("Game initialisation sequence event loop starting.")
    while running:
        # Handle events
        for event in pygame.event.get():

            # check if the window is closed
            if event.type == pygame.QUIT:
                logger.info("Quit event detected. Closing the game.")
                # if so, end the script by breaking the while loop
                running = False
                # Quit Pygame
                pygame.quit()
                sys.exit()

            # check if a click event occured
            if event.type == pygame.MOUSEBUTTONDOWN:
                click_pos = event.pos
                logger.debug(f"CLICK at {click_pos}")
            else:
                click_pos = None

            # check if any buttons were pressed
            if event.type == pygame.KEYDOWN:
                key_press = key_interpreter(event.key)
                logger.debug(f"KEYSTROKE with {key_press}")
            else:
                key_press = None

        # update display
        try:
            game = game.render(screen, click_pos, key_press)

        except SystemExit:
            logger.info("Force closing the game.")
            sys.exit()

        except BaseException:
            logger.error(traceback.format_exc())
            logger.info("Closing the game due to unexpected error.")
            running = False
            pygame.quit()
            sys.exit()

        # Update the display
        pygame.display.update()

        # Limit frame rate to set FPS
        clock.tick(settings.CLOCKSPEED)


if __name__ == "__main__":
    main()
