"""Utilities for the Cryptids game."""
import logging
import pygame
import re
import sys

from cryptids import settings as get

# get the logger
logger = logging.getLogger(__name__)

if get.VERBOSE:
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)


def clean_string(string: str) -> str:
    r"""
    Remove punctuation from a string.

    [   #Character block start.
    ^   #Not these characters (letters, numbers).
    \w  #Word characters.
    \s  #Space characters.
    ]   #Character block end.

    Parameters
    ----------
    string : str
        The string for cleaning.

    Returns
    -------
    cleaned_string : str
        The cleaned string.

    """
    check_type(string, "string", str)
    return re.sub(r'[^\w\s]', '', string)


def check_type(var, varname: str, vartype) -> None:
    """
    Check the type of a variable against it's intended type.

    This variable takes var and checks it against var type using the isinstance
    technique, it then produces a standardised error message in the outcome
    that the variable is not the correct variable.

    Parameters
    ----------
    var : any type
        An instance of the variable you wish to check
    varname : str
        A string that is the __name__ of the variable.
    vartype : any type
        An instance of the type of variable you expect var to be.

    Returns
    -------
    None

    Example
    -------
    import numpy as np
    a = "not a numpy array"
    check_type(a, "a", str) --> nothing happens
    check_type(a, "a", np.ndarray) --> raises Type Error
    """
    # check inputs
    if not isinstance(varname, str):
        raise TypeError(
            f"Input variable '{varname}' should be of type str is in fact of type: {type(varname)}")

    # perform the check on the requested variable and vartype
    if not isinstance(var, vartype):
        raise TypeError(
            f"Input variable '{varname}' should be of type {vartype} is in fact of type: {type(var)}")
    return None


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
    return None
