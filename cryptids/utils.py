# -*- coding: utf-8 -*-
"""
Created on Sat Dec 17 02:46:54 2022

@author: jamie
"""
import pygame


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
