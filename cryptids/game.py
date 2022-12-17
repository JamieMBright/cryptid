"""
The main Game class.

This controls all the sequences of the game and deals with their rendering.
"""
import sys

import pygame

from cryptids import settings, utils
from cryptids.button import Button


class GameWrapper(object):
    """Wrapper that renders the game."""

    def __init__(self):
        self.game_status = settings.DEFAULT_STATUS
        self.intro_sequence_position = 1
        self.outro_sequence_position = 1
        self.intro_counter = 0
        self.outro_counter = 0
        self.focus_pos = [0, 0]

    def render(self, screen, click_pos, key_press):
        """Select the game status to render."""
        if self.game_status == settings.STATUS_INTRO:
            self._render_intro(screen, click_pos, key_press)
        elif self.game_status == settings.STATUS_HOME:
            self._render_home_screen(screen, click_pos, key_press)
        elif self.game_status == settings.STATUS_SETTINGS:
            self._render_settings_screen(screen, click_pos, key_press)
        elif self.game_status == settings.STATUS_PLAY:
            self._render_play_mode(screen, click_pos, key_press)
        elif self.game_status == settings.STATUS_OUTRO:
            self._render_outro(screen, click_pos, key_press)
        elif self.game_status not in settings.GAME_STATUSES:
            raise ValueError(f"Unrecognised game_status: {self.game_status}")

    def _render_intro(self, screen, click_pos, key_press):
        """
        "Draw the intro.

        The intro has three sequences:

            sequence 1) Cryptids title text appears
            sequence 2) Developer credit
            sequence 3) Cryptid logo

        """
        # if we are in the title screen
        if self.intro_sequence_position == 1:
            if self.intro_counter < settings.CLOCKSPEED * settings.TITLE_DURATION:
                # title text
                screen.fill(settings.TITLE_SCREEN_BACKGROUND_COLOR)
                font = pygame.font.Font(settings.TITLE_SCREEN_FONT, settings.TITLE_SCREEN_FONT_SIZE)
                text = font.render(settings.TITLE_SCREEN_TEXT, True, settings.TITLE_SCREEN_TEXT_COLOUR)
                textRect = text.get_rect()
                textRect.center = (settings.WINWIDTH // 2, settings.WINHEIGHT // 2)
                screen.blit(text, textRect)
                self.intro_counter += 1
            else:
                # else the title sequence must end
                self.intro_sequence_position += 1
                self.intro_counter = 0

        # else if we are on the developer credit
        elif self.intro_sequence_position == 2:
            if self.intro_counter < settings.CLOCKSPEED * settings.CREDIT_DURATION:
                screen.fill(settings.CREDIT_SCREEN_BACKGROUND_COLOR)
                font = pygame.font.Font(settings.CREDIT_SCREEN_FONT, settings.CREDIT_SCREEN_FONT_SIZE)
                text = font.render(settings.CREDIT_SCREEN_TEXT, True, settings.CREDIT_SCREEN_TEXT_COLOUR)
                textRect = text.get_rect()
                textRect.center = settings.CENTRE
                screen.blit(text, textRect)
                self.intro_counter += 1
            else:
                # else the title sequence must end
                self.intro_sequence_position += 1
                self.intro_counter = 0

        elif self.intro_sequence_position == 3:
            if self.intro_counter < settings.CLOCKSPEED * settings.LOGO_DURATION:
                screen.fill(settings.LOGO_SCREEN_BACKGROUND_COLOR)
                logo = pygame.image.load(settings.LOGO_SCREEN_IMAGE_PATH).convert_alpha()
                logo = utils.reshape_keep_aspect(logo, new_height=settings.WINHEIGHT * settings.LOGO_HEIGHT_RELATIVE_TO_SCREEN_HEIGHT)
                logoRect = logo.get_rect()
                logoRect.center = settings.CENTRE
                screen.blit(logo, logoRect)

                self.intro_counter += 1
            else:
                # else the title sequence must end
                self.game_status = settings.STATUS_HOME
        return self

    def _render_home_screen(self, screen, click_pos, key_press):
        """Draw the home screen."""
        def _quit_button_action():
            self.game_status = settings.STATUS_OUTRO

        def _play_button_action():
            self.game_status = settings.STATUS_PLAY

        def _settings_button_action():
            self.game_status = settings.STATUS_SETTINGS

        #  background imagery
        screen.fill(settings.LOGO_SCREEN_BACKGROUND_COLOR)
        logo = pygame.image.load(settings.LOGO_SCREEN_IMAGE_PATH).convert_alpha()
        logo = utils.reshape_keep_aspect(logo, new_height=settings.WINHEIGHT * settings.LOGO_HEIGHT_RELATIVE_TO_SCREEN_HEIGHT)
        logoRect = logo.get_rect()
        logoRect.center = settings.CENTRE
        screen.blit(logo, logoRect)

        # buttons
        total_buttons = 3
        gap = (settings.WINWIDTH - (total_buttons + 1) * settings.BUTTON_DEFAULT_WIDTH) // (total_buttons + 1)

        # play button -> move to play screen
        x = gap
        y = int(settings.WINHEIGHT * settings.HOME_BUTTON_Y_REL - settings.BUTTON_DEFAULT_HEIGHT // 2)
        play_button = Button(text="PLAY", x=x, y=y)
        screen.blit(play_button.surface, (x, y))

        # settings button -> move to settings screen
        x = gap * 2 + settings.BUTTON_DEFAULT_WIDTH
        settings_button = Button(text="SETTINGS", x=x, y=y, width=int(settings.BUTTON_DEFAULT_WIDTH * 2))
        screen.blit(settings_button.surface, (x, y))

        # quit button -> exit the game
        x = gap * 3 + settings.BUTTON_DEFAULT_WIDTH * 3
        quit_button = Button(text="QUIT", x=x, y=y)
        screen.blit(quit_button.surface, (x, y))

        # click actions
        if quit_button.was_clicked(click_pos):
            _quit_button_action()
        elif play_button.was_clicked(click_pos):
            _play_button_action()
        elif settings_button.was_clicked(click_pos):
            _settings_button_action()

    def _render_settings_screen(self, screen, click_pos, key_press):
        """Draw the settings screen."""

        def _back_button_action():
            self.game_status = settings.STATUS_HOME

        #  background imagery
        screen.fill(settings.LOGO_SCREEN_BACKGROUND_COLOR)
        logo = pygame.image.load(settings.LOGO_SCREEN_IMAGE_PATH).convert_alpha()
        logo.fill((255, 255, 255, settings.SETTINGS_LOGO_IMG_ALPHA), None, pygame.BLEND_RGBA_MULT)
        logo = utils.reshape_keep_aspect(logo, new_height=settings.WINHEIGHT * settings.LOGO_HEIGHT_RELATIVE_TO_SCREEN_HEIGHT)
        logoRect = logo.get_rect()
        logoRect.center = settings.CENTRE
        screen.blit(logo, logoRect)

        # buttons
        # back button -> move to home screen
        total_buttons = 3
        x = (settings.WINWIDTH - total_buttons * settings.BUTTON_DEFAULT_WIDTH) // (total_buttons + 1)
        y = int(settings.WINHEIGHT * settings.HOME_BUTTON_Y_REL - settings.BUTTON_DEFAULT_HEIGHT // 2)
        back_button = Button(text="BACK", x=x, y=y)
        screen.blit(back_button.surface, (x, y))

        # click actions
        if back_button.was_clicked(click_pos):
            _back_button_action()

    def _render_outro(self, screen, click_pos, key_press):
        """
        "Draw the outtro.

        The outro has two sequence:

            sequence 1) Cryptid logo
            sequence 2) Thank you + credit

        """
        # if we are in the title screen
        if self.outro_sequence_position == 1:
            if self.outro_counter < settings.CLOCKSPEED * settings.LOGO_DURATION:
                # Logo only
                screen.fill(settings.LOGO_SCREEN_BACKGROUND_COLOR)
                logo = pygame.image.load(settings.LOGO_SCREEN_IMAGE_PATH).convert_alpha()
                logo = utils.reshape_keep_aspect(logo, new_height=settings.WINHEIGHT * settings.LOGO_HEIGHT_RELATIVE_TO_SCREEN_HEIGHT)
                logoRect = logo.get_rect()
                logoRect.center = settings.CENTRE
                screen.blit(logo, logoRect)
                self.outro_counter += 1
            else:
                # else the title sequence must end
                self.outro_sequence_position += 1
                self.outro_counter = 0

        # else if we are on the developer credit
        elif self.outro_sequence_position == 2:
            if self.outro_counter < settings.CLOCKSPEED * settings.OUTRO_DURATION:
                screen.fill(settings.OUTRO_SCREEN_BACKGROUND_COLOR)
                # first line
                font1 = pygame.font.Font(settings.OUTRO_SCREEN_FONT, settings.OUTRO_SCREEN_FONT_SIZE1)
                text1 = font1.render(settings.OUTRO_SCREEN_TEXT1, True, settings.OUTRO_SCREEN_TEXT_COLOUR)
                textRect1 = text1.get_rect()
                textRect1.center = (settings.X50, settings.Y75)
                screen.blit(text1, textRect1)

                # second line
                font2 = pygame.font.Font(settings.OUTRO_SCREEN_FONT, settings.OUTRO_SCREEN_FONT_SIZE2)
                text2 = font2.render(settings.OUTRO_SCREEN_TEXT2, True, settings.OUTRO_SCREEN_TEXT_COLOUR)
                textRect2 = text2.get_rect()
                textRect2.center = (settings.X50, settings.Y50)
                screen.blit(text2, textRect2)

                # third line
                font3 = pygame.font.Font(settings.OUTRO_SCREEN_FONT, settings.OUTRO_SCREEN_FONT_SIZE3)
                text3 = font3.render(settings.OUTRO_SCREEN_TEXT3, True, settings.OUTRO_SCREEN_TEXT_COLOUR)
                textRect3 = text3.get_rect()
                textRect3.center = (settings.X50, settings.Y25)
                screen.blit(text3, textRect3)

                self.outro_counter += 1

            else:
                pygame.quit()
                sys.exit()

    def _render_play_mode(self, screen, click_pos, key_press):
        """Draw the play screen."""

        def _back_button_action():
            self.game_status = settings.STATUS_HOME

        #  background imagery
        screen.fill(settings.LOGO_SCREEN_BACKGROUND_COLOR)
        logo = pygame.image.load(settings.LOGO_SCREEN_IMAGE_PATH).convert_alpha()
        logo.fill((255, 255, 255, settings.SETTINGS_LOGO_IMG_ALPHA), None, pygame.BLEND_RGBA_MULT)
        logo = utils.reshape_keep_aspect(logo, new_height=settings.WINHEIGHT * settings.LOGO_HEIGHT_RELATIVE_TO_SCREEN_HEIGHT)
        logoRect = logo.get_rect()
        logoRect.center = settings.CENTRE
        screen.blit(logo, logoRect)

        # buttons
        # back button -> move to home screen
        total_buttons = 3
        x = (settings.WINWIDTH - total_buttons * settings.BUTTON_DEFAULT_WIDTH) // (total_buttons + 1)
        y = int(settings.WINHEIGHT * settings.HOME_BUTTON_Y_REL - settings.BUTTON_DEFAULT_HEIGHT // 2)
        back_button = Button(text="BACK", x=x, y=y)
        screen.blit(back_button.surface, (x, y))

        # click actions
        if back_button.was_clicked(click_pos):
            _back_button_action()
