"""Utilities for the Cryptids game."""
import logging
import pygame
import sys

from cryptids import settings

# get the logger
logger = logging.getLogger(__name__)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


def reshape_keep_aspect(img, new_height=None, new_width=None):
    """
    Resize a pygame image whilst retaining the aspect ratio.

    Can only provide one of new_height or new_width. Must provide at least one.

    Parameters
    ----------
    img : pygame image
        an image loaded from pygame.
    new_height : (float, int), optional
        Target height. The default is None.
    new_width : (float, int), optional
        Target width. The default is None.

    Raises
    ------
    ValueError
        If neither or both new height and width are provided..

    Returns
    -------
    img : pygame image
        The reshaped image.

    """
    if new_height is None and new_width is None:
        raise ValueError("need at least one new height/width, both were None.")

    elif new_height is not None and new_width is not None:
        raise ValueError("cannot define both new height and width, can only suggest one.")
    width = img.get_width()
    height = img.get_height()
    aspect = width / height

    if new_height is not None:
        new_width = new_height * aspect
    if new_width is not None:
        new_height = new_width / aspect

    img = pygame.transform.scale(img, (int(new_width), int(new_height)))
    return img


def delay_n_frames(num_frames: int,
                   clockspeed: int):
    """
    Delay a fixed number of frames.

    Parameters
    ----------
    num_frames : int
        Number of framaes to delay.

    Returns
    -------
    None.

    """
    logger.debug(f"Delaying for {num_frames} frames")
    # initialaise the frame count
    frame_count = 0
    # initialise the infinite loop
    running = True

    # Set up game clock
    clock = pygame.time.Clock()
    # enter the event loop
    while running and frame_count < num_frames:
        # Check for quit events, which would override this delay
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # break the loop if a quit event
                running = False
            # increment the frame count
        frame_count += 1

        # tick the clock
        clock.tick(clockspeed)
        # Update the display
        pygame.display.update()
    logger.debug("Finished delaying.")
    return None
