# -*- coding: utf-8 -*-
"""
Created on Sat Dec 17 09:25:35 2022

@author: jamie
"""

"""Button."""
import logging
from os import PathLike
from typing import Tuple

import pygame

from cryptids import settings, utils
from cryptids.loggingdecorator import log

# get the logger
logger = logging.getLogger(__name__)


class Button():
    """
    Generate a button.

    Parameters
    ----------
        x, int,
            x position for top right of button (pixels)
        y, int,
            y position for top right of button (pixels)
        width, int,
            Width of the button (pixels)
        height: int,
            Height of the button (pixels)
        text: str,
            The text to display on the button.
        font_name: (str, PathLike),
            Font name or path to font .ttf file.
        font_size: int,
            Size of the font
        font_colour: (str, Tuple[int, int, int]),
            Colour of the font as stored RGB or direct RGB.
        bg_color: (str, Tuple[int, int, int]),
            Colour of the background.
        bg_image: PathLike,
            Path to the image for the button.

    Methods
    -------
        _create_surface()
            Build the button surface.

        was_selected()
            Is the button selected.

    Returns
    -------
        None
    """

    def __init__(self,
                 x: int = 0,
                 y: int = 0,
                 width: int = settings.BUTTON_DEFAULT_WIDTH,
                 height: int = settings.BUTTON_DEFAULT_HEIGHT,
                 text: str = None,
                 font_name: (str, PathLike) = settings.BUTTON_DEFAULT_FONTNAME,
                 font_size: int = settings.BUTTON_DEFAULT_FONTSIZE,
                 font_colour: (str, Tuple[int, int, int]) = settings.BUTTON_DEFAULT_FONTCOLOUR,
                 bg_colour: (str, Tuple[int, int, int]) = settings.BUTTON_DEFAULT_BGCOLOUR,
                 bg_colour_highlighted: (str, Tuple[int, int, int]) = settings.BUTTON_DEFAULT_BACKGROUND_HIGHLIGHTED,
                 bg_colour_clicked: (str, Tuple[int, int, int]) = settings.BUTTON_DEFAULT_BACKGROUND_CLICKED,
                 bg_image: PathLike = None,
                 border_thickness: int = settings.BUTTON_DEFAULT_BORDER_THICKNESS,
                 border_colour: (str, Tuple[int, int, int]) = settings.BUTTON_DEFAULT_BORDER_COLOUR,
                 border_colour_highlighted: (str, Tuple[int, int, int]) = settings.BUTTON_DEFAULT_BORDER_HIGHLIGHTED,
                 click_pos: Tuple[int, int] = None,
                 toggleable: bool = False,
                 toggle_hover_bg_colour: (str, Tuple[int, int, int]) = settings.BUTTON_DEFAULT_TOGGLE_HOVER_BG_COLOUR,
                 toggled_bg_colour: (str, Tuple[int, int, int]) = settings.BUTTON_DEFAULT_TOGGLED_BG_COLOUR
                 ):

        self.rect = pygame.Rect(x, y, width, height)  # left, top, width, height
        self.bg_colour = bg_colour
        self.bg_colour_highlighted = bg_colour_highlighted
        self.bg_image = bg_image
        self.text = text
        self.font_name = font_name
        self.font_size = font_size
        self.font_colour = font_colour
        self.border_thickness = border_thickness
        self.border_colour = border_colour
        self.border_colour_highlighted = border_colour_highlighted
        self.bg_colour_clicked = bg_colour_clicked
        self.toggle_hover_bg_colour = toggle_hover_bg_colour
        self.toggled_bg_colour = toggled_bg_colour
        self.clicked = False
        self.click_pos = click_pos
        self.toggleable = toggleable
        self.toggle = False
        self.surface = self._render()

    def _render(self):
        # Create a new surface with the button's dimensions
        surface = pygame.Surface((self.rect.width, self.rect.height))

        # get the background colour if highlighted
        if self.is_mouse_hovering() and self.toggleable:
            bg_col = self.toggle_hover_bg_colour
        elif self.is_mouse_hovering():
            bg_col = self.bg_colour_highlighted
        # else default background colour
        else:
            if self.toggle:
                bg_col = self.toggled_bg_colour
            else:
                bg_col = self.bg_colour
        # get the background cover if clicked
        if self.was_clicked(self.click_pos):
            bg_col = self.bg_colour_clicked

            # Fill the surface with the background color or image
        if self.bg_image:
            surface.blit(self.bg_image, (0, 0))
        else:
            surface.fill(bg_col)

        # Draw the button's text on the surface
        if self.text:
            font = pygame.font.Font(self.font_name, self.font_size)
            text = font.render(self.text, True, self.font_colour)
            text_rect = text.get_rect()
            text_rect.center = (self.rect.width // 2, self.rect.height // 2)
            surface.blit(text, text_rect)

        return surface

    def is_mouse_hovering(self):
        """Return True if mouse is hovering."""
        # get current mouse position
        return self.rect.collidepoint(pygame.mouse.get_pos())

    def was_clicked(self, click_pos):
        """Return True if mouse clicked on button."""
        # get current mouse position
        if click_pos is not None:
            if self.is_mouse_hovering() and self.rect.collidepoint(click_pos):
                return True
            else:
                return False
        else:
            return False

    def toggle_button(self):
        """Change toggle state."""
        self.toggle = not self.toggle
        return None
