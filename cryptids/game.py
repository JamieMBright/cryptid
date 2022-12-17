# -*- coding: utf-8 -*-
"""
Created on Sat Dec 17 01:39:53 2022

@author: jamie
"""

"""
The main Game class.

This controls all the sequences of the game and deals with their rendering.
"""
import pygame
from cryptids import settings, utils


class Game(object):
    def __init__(self):
        self.game_status = settings.DEFAULT_STATUS
        self.intro_sequence_position = 1
        self.counter = 0

    def render(self, screen):
        if self.game_status == "intro":
            self._render_intro(screen)
        elif self.game_status == "home_screen":
            self._render_home_screen(screen)
        elif self.gamestatus == "duel":
            self._render_duel(screen)
        elif self.game_status not in settings.GAME_STATUSES:
            raise ValueError(f"Unrecognised game_status: {self.game_status}")

    def _render_intro(self, screen):
        """
        "Draw the intro.

        The intro has three sequences:

            sequence 1) Cryptids title text appears
            sequence 2) Developer credit
            sequence 3) Cryptid logo

        """
        # if we are in the title screen
        if self.intro_sequence_position == 1:
            if self.counter < settings.CLOCKSPEED * settings.TITLE_DURATION:
                # title text
                screen.fill(settings.TITLE_SCREEN_BACKGROUND_COLOR)
                font = pygame.font.Font(settings.TITLE_SCREEN_FONT, settings.TITLE_SCREEN_FONT_SIZE)
                text = font.render(settings.TITLE_SCREEN_TEXT, True, settings.TITLE_SCREEN_TEXT_COLOUR)
                textRect = text.get_rect()
                textRect.center = (settings.WINWIDTH // 2, settings.WINHEIGHT // 2)
                screen.blit(text, textRect)
                self.counter += 1
            else:
                # else the title sequence must end
                self.intro_sequence_position += 1
                self.counter = 0

        # else if we are on the developer credit
        elif self.intro_sequence_position == 2:
            if self.counter < settings.CLOCKSPEED * settings.CREDIT_DURATION:
                screen.fill(settings.CREDIT_SCREEN_BACKGROUND_COLOR)
                font = pygame.font.Font(settings.CREDIT_SCREEN_FONT, settings.CREDIT_SCREEN_FONT_SIZE)
                text = font.render(settings.CREDIT_SCREEN_TEXT, True, settings.CREDIT_SCREEN_TEXT_COLOUR)
                textRect = text.get_rect()
                textRect.center = settings.CENTRE
                screen.blit(text, textRect)
                self.counter += 1
            else:
                # else the title sequence must end
                self.intro_sequence_position += 1
                self.counter = 0

        elif self.intro_sequence_position == 3:
            if self.counter < settings.CLOCKSPEED * settings.LOGO_DURATION:
                screen.fill(settings.LOGO_SCREEN_BACKGROUND_COLOR)
                logo = pygame.image.load(settings.LOGO_SCREEN_IMAGE_PATH).convert_alpha()
                logo = utils.reshape_keep_aspect(logo, new_height=settings.WINHEIGHT * settings.LOGO_HEIGHT_RELATIVE_TO_SCREEN_HEIGHT)
                logoRect = logo.get_rect()
                logoRect.center = settings.CENTRE
                screen.blit(logo, logoRect)

                self.counter += 1
            else:
                # else the title sequence must end
                self.game_status = "home_screen"
        return self

    def _render_home_screen(self, screen):
        """Draw the home screen."""
        #  use the logo again
        screen.fill(settings.LOGO_SCREEN_BACKGROUND_COLOR)
        logo = pygame.image.load(settings.LOGO_SCREEN_IMAGE_PATH).convert_alpha()
        logo = utils.reshape_keep_aspect(logo, new_height=settings.WINHEIGHT * settings.LOGO_HEIGHT_RELATIVE_TO_SCREEN_HEIGHT)
        logoRect = logo.get_rect()
        logoRect.center = settings.CENTRE
        screen.blit(logo, logoRect)
        # make the buttons appear
        # Play button
        font = pygame.font.Font(settings.HOME_SCREEN_FONT, settings.HOME_SCREEN_FONT_SIZE)
        text = font.render("PLAY", True, settings.HOME_SCREEN_TEXT_COLOUR)
        textRect = text.get_rect()
        textRect.center = (int(settings.WINWIDTH * settings.HOME_BUTTON_X_REL), int(settings.WINHEIGHT * settings.HOME_BUTTON_X_REL))
        screen.blit(text, textRect)
        # Quit button
        font = pygame.font.Font(settings.HOME_SCREEN_FONT, settings.HOME_SCREEN_FONT_SIZE)
        text = font.render("QUIT", True, settings.HOME_SCREEN_TEXT_COLOUR)
        textRect = text.get_rect()
        textRect.center = (int(settings.WINWIDTH - settings.WINWIDTH * settings.HOME_BUTTON_X_REL), int(settings.WINHEIGHT * settings.HOME_BUTTON_X_REL))
        screen.blit(text, textRect)

    def _render_duel(self, screen):
        """Draw the duel."""
        raise NotImplementedError("yet to build duel")
