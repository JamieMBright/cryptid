"""Button class."""
import logging
from os import PathLike
from typing import Tuple
import sys

import pygame

from cryptids import settings as get
from cryptids import utils

# get the logger
logger = logging.getLogger(__name__)

if get.VERBOSE:
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)


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
        access : bool,
            Whether or not the button can be clicked/hovered.
        bg_colour_disabled : (str, Tuple[int, int, int]),
            The background colour if the button is disabled.

    Methods
    -------
        _create_surface()
            Build the button surface.

        was_selected()
            Is the button selected.

        toggle_access()
            Switch the access to on (if off) or off (if on).

        get_access()
            Get the current access state.

        set_access(bool)
            Set the access to a implicit state.

    Returns
    -------
        None
    """

    def __init__(self,
                 x: int = 0,
                 y: int = 0,
                 width: int = get.BUTTON_DEFAULT_WIDTH,
                 height: int = get.BUTTON_DEFAULT_HEIGHT,
                 text: str = "",
                 font_name: (str, PathLike) = get.BUTTON_DEFAULT_FONTNAME,
                 font_name_textbox: (str, PathLike) = get.BUTTON_INTPUTTEXT_FONTNAME,
                 font_size: int = get.BUTTON_DEFAULT_FONTSIZE,
                 font_size_textbox: int = get.BUTTON_INTPUTTEXT_FONTSIZE,
                 font_colour: (str, Tuple[int, int, int]) = get.BUTTON_DEFAULT_FONTCOLOUR,
                 font_colour_textbox: (str, Tuple[int, int, int]) = get.BUTTON_INPUTTEXT_FONTCOLOUR,
                 font_colour_active: (str, Tuple[int, int, int]) = get.BUTTON_ACTIVE_TEXT_COLOUR,
                 bg_colour: (str, Tuple[int, int, int]) = get.BUTTON_DEFAULT_BGCOLOUR,
                 bg_colour_highlighted: (str, Tuple[int, int, int]) = get.BUTTON_DEFAULT_BACKGROUND_HIGHLIGHTED,
                 bg_colour_clicked: (str, Tuple[int, int, int]) = get.BUTTON_DEFAULT_BACKGROUND_CLICKED,
                 bg_colour_active: (str, Tuple[int, int, int]) = get.BUTTON_ACTIVE_BACKGROUND_COLOUR,
                 bg_colour_toggle_hover: (str, Tuple[int, int, int]) = get.BUTTON_DEFAULT_TOGGLE_HOVER_BG_COLOUR,
                 bg_colour_toggled: (str, Tuple[int, int, int]) = get.BUTTON_DEFAULT_TOGGLED_BG_COLOUR,
                 bg_colour_textbox: (str, Tuple[int, int, int]) = get.BUTTON_INTPUTTEXT_BACKGROUND_COLOUR,
                 bg_colour_disabled: (str, Tuple[int, int, int]) = get.BUTTON_DEFAULT_BACKGROUND_DISABLED,
                 bg_image: PathLike = None,
                 border_thickness: int = get.BUTTON_DEFAULT_BORDER_THICKNESS,
                 border_colour: (str, Tuple[int, int, int]) = get.BUTTON_DEFAULT_BORDER_COLOUR,
                 border_colour_highlighted: (str, Tuple[int, int, int]) = get.BUTTON_DEFAULT_BORDER_HIGHLIGHTED,
                 click_pos: Tuple[int, int] = None,
                 toggleable: bool = False,
                 click_event: bool = False,
                 access: bool = True,
                 input_text: bool = False,
                 allow_reshape: bool = False,
                 private: bool = False
                 ):

        self.x = x
        self.y = y
        self.width = width
        self.height = height
        if input_text:
            self.bg_colour = bg_colour_textbox
            self.font_name = font_name_textbox
            self.font_size = font_size_textbox
            self.font_colour = font_colour_textbox
            self.font_colour_active = font_colour_active
        else:
            self.bg_colour = bg_colour
            self.font_name = font_name
            self.font_size = font_size
            self.font_colour = font_colour

        self.bg_colour_highlighted = bg_colour_highlighted
        self.bg_colour_clicked = bg_colour_clicked
        self.bg_colour_disabled = bg_colour_disabled
        self.bg_colour_active = bg_colour_active
        self.bg_colour_toggle_hover = bg_colour_toggle_hover
        self.bg_colour_toggled = bg_colour_toggled
        self.bg_image = bg_image
        if private:
            self.text = "*" * len(text)
        else:
            self.text = text
        self.border_thickness = border_thickness
        self.border_colour = border_colour
        self.border_colour_highlighted = border_colour_highlighted
        self.clicked = False
        self.click_pos = click_pos
        self.toggleable = toggleable
        self.toggle = False
        self.click_event = click_event
        self.access = access
        self.allow_reshape = allow_reshape
        self.active = False
        self.private = private

        self.surface = self._render()

    def _render(self):

        if self.active:
            font_colour = self.font_colour_active
        else:
            font_colour = self.font_colour

        # make the text surface
        font = pygame.font.Font(self.font_name, self.font_size)
        text_surface = font.render(self.text, True, font_colour)

        # Resize the box if the text is too long.
        if self.allow_reshape:
            self.width = text_surface.get_width()
        else:
            while text_surface.get_width() >= self.width:
                self.font_size -= 2
                font = pygame.font.Font(self.font_name, self.font_size)
                text_surface = font.render(self.text, True, font_colour)

            # get the box surface
        box_surface = pygame.Surface((self.width + get.BUTTON_DEFAULT_TEXT_X_BUFFER, self.height + get.BUTTON_DEFAULT_TEXT_Y_BUFFER))

        # make the box a property
        self.box_surface_rect = box_surface.get_rect(left=self.x, top=self.y)

        # change background colour based on event
        # events for colour in order are:
        if not self.access:
            # if the button is not accessible, then it is disabled.
            bg_col = self.bg_colour_disabled
        elif self.active:
            # if the button is actively in use (e.g. text input)
            bg_col = self.bg_colour_active
        elif self.was_clicked(self.click_pos):
            # else if the button has been clicked, and we are registering a delay
            bg_col = self.bg_colour_clicked
        elif self.is_mouse_hovering():
            # else if th mouse is hovering over the button and we wish to show what will be clicked
            bg_col = self.bg_colour_highlighted
        elif self.is_mouse_hovering() and self.toggleable:
            # likewise if the mouse is hovering, and the button can be toggled.
            bg_col = self.bg_colour_toggle_hover
        elif self.toggle:
            # else if the button has been toggled on (default if off)
            bg_col = self.bg_colour_toggled
        else:
            # else no modifiers present, so default to the normal colour
            bg_col = self.bg_colour

        # Fill the surface with the background color or image
        if self.bg_image:
            box_surface.blit(self.bg_image, (0, 0))
        else:
            box_surface.fill(bg_col)

        # blit text to centre of box
        center_x = box_surface.get_width() // 2
        center_y = box_surface.get_height() // 2
        box_surface.blit(text_surface, (center_x - text_surface.get_width() // 2, center_y - text_surface.get_height() // 2))

        return box_surface

    def is_mouse_hovering(self):
        """Return True if mouse is hovering."""
        # get current mouse position
        return self.box_surface_rect.collidepoint(pygame.mouse.get_pos())

    def was_clicked(self, click_pos):
        """Return True if mouse clicked on button."""
        # get current mouse position
        if click_pos is not None:
            if self.is_mouse_hovering() and self.box_surface_rect.collidepoint(click_pos) and self.click_event and self.access:
                return True
            else:
                return False
        else:
            return False

    def toggle_button(self):
        """Change toggle state."""
        self.toggle = not self.toggle

    def toggle_access(self):
        """Enable or disable the button."""
        self.access = not self.access

    def set_access(self, setter: bool):
        """Set the access implicitly."""
        utils.check_type(setter, "setter", bool)
        self.access = setter

    def get_access(self):
        """Get the access."""
        return self.access

    def text_input_action(self, screen):
        """Handle text input."""
        # set status to active
        self.active = True
        # set the loop break
        running = True
        # initialize the text
        text = ""

        # Set up game clock
        clock = pygame.time.Clock()
        # enter the event loop
        while running:
            events = pygame.event.get()
            # flags
            self.click_event = False
            click_pos = None
            # if we have any, process them.
            if events:
                for event in events:

                    # check if the window is closed
                    match event.type:
                        case pygame.QUIT:
                            logger.info("Quit event detected. Closing the game.")
                            # if so, end the script by breaking the while loop
                            running = False
                            # Quit Pygame
                            pygame.quit()
                            sys.exit()

                        # check if a click event occured
                        case pygame.MOUSEBUTTONDOWN:
                            click_pos = event.pos
                            logger.debug(f"CLICK at {click_pos}")
                            self.click_event = True
                            if not self.was_clicked(click_pos):
                                # if the click was NOT on the text box, assume end.
                                running = False

                        case pygame.KEYDOWN:
                            logger.debug(f"KEYSTROKE with {event.unicode}")
                            if event.key in [pygame.K_RETURN, pygame.K_ESCAPE, pygame.K_TAB]:
                                # we assume they are content with this.
                                running = False

                            elif event.key == pygame.K_BACKSPACE:
                                text = text[:-1]

                            else:
                                text += event.unicode

            if self.private:
                self.text = "*" * len(text)
            else:
                self.text = text
            button_box = self._render()
            screen.blit(button_box, (self.x, self.y))

            # render the text to the box.
            # Update the display
            pygame.display.update()

            # Limit frame rate to set FPS
            clock.tick(get.CLOCKSPEED)

        self.active = False
        return text
