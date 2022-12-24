"""
The main Game class.

This controls all the sequences of the game and deals with their rendering.
"""
import sys

import pygame

import cryptids.settings as get
from cryptids import utils
from cryptids.button import Button


class GameWrapper(object):
    """Wrapper that renders the game."""

    def __init__(self):
        self.game_status = get.DEFAULT_STATUS
        self.intro_sequence_position = 1
        self.outro_sequence_position = 1
        self.intro_counter = 0
        self.outro_counter = 0
        self.focus_pos = [0, 0]

    def render(self, screen, click_pos, key_press):
        """Select the game status to render."""
        if self.game_status == get.STATUS_INTRO:
            self._render_intro(screen, click_pos, key_press)
        elif self.game_status == get.STATUS_HOME:
            self._render_home_screen(screen, click_pos, key_press)
        elif self.game_status == get.STATUS_SETTINGS:
            self._render_settings_screen(screen, click_pos, key_press)
        elif self.game_status == get.STATUS_PLAY:
            self._render_play_mode(screen, click_pos, key_press)
        elif self.game_status == get.STATUS_OUTRO:
            self._render_outro(screen, click_pos, key_press)
        elif self.game_status not in get.GAME_STATUSES:
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
            if self.intro_counter < get.CLOCKSPEED * get.TITLE_DURATION:
                # title text
                screen.fill(get.TITLE_SCREEN_BACKGROUND_COLOR)
                font = pygame.font.Font(get.TITLE_SCREEN_FONT, get.TITLE_SCREEN_FONT_SIZE)
                text = font.render(get.TITLE_SCREEN_TEXT, True, get.TITLE_SCREEN_TEXT_COLOUR)
                textRect = text.get_rect()
                textRect.center = (get.WINWIDTH // 2, get.WINHEIGHT // 2)
                screen.blit(text, textRect)
                self.intro_counter += 1
            else:
                # else the title sequence must end
                self.intro_sequence_position += 1
                self.intro_counter = 0

        # else if we are on the developer credit
        elif self.intro_sequence_position == 2:
            if self.intro_counter < get.CLOCKSPEED * get.CREDIT_DURATION:
                screen.fill(get.CREDIT_SCREEN_BACKGROUND_COLOR)
                font = pygame.font.Font(get.CREDIT_SCREEN_FONT, get.CREDIT_SCREEN_FONT_SIZE)
                text = font.render(get.CREDIT_SCREEN_TEXT, True, get.CREDIT_SCREEN_TEXT_COLOUR)
                textRect = text.get_rect()
                textRect.center = get.CENTRE
                screen.blit(text, textRect)
                self.intro_counter += 1
            else:
                # else the title sequence must end
                self.intro_sequence_position += 1
                self.intro_counter = 0

        elif self.intro_sequence_position == 3:
            if self.intro_counter < get.CLOCKSPEED * get.LOGO_DURATION:
                screen.fill(get.LOGO_SCREEN_BACKGROUND_COLOR)
                logo = pygame.image.load(get.LOGO_SCREEN_IMAGE_PATH).convert_alpha()
                logo = utils.reshape_keep_aspect(logo, new_height=get.WINHEIGHT * get.LOGO_HEIGHT_RELATIVE_TO_SCREEN_HEIGHT)
                logoRect = logo.get_rect()
                logoRect.center = get.CENTRE
                screen.blit(logo, logoRect)

                self.intro_counter += 1
            else:
                # else the title sequence must end
                self.game_status = get.STATUS_HOME
        return self

    def _render_home_screen(self, screen, click_pos, key_press):
        """Draw the home screen."""
        def _quit_button_action():
            self.game_status = get.STATUS_OUTRO

        def _play_button_action():
            self.game_status = get.STATUS_PLAY

        def _settings_button_action():
            self.game_status = get.STATUS_SETTINGS

        #  background imagery
        screen.fill(get.LOGO_SCREEN_BACKGROUND_COLOR)
        logo = pygame.image.load(get.LOGO_SCREEN_IMAGE_PATH).convert_alpha()
        logo = utils.reshape_keep_aspect(logo, new_height=get.WINHEIGHT * get.LOGO_HEIGHT_RELATIVE_TO_SCREEN_HEIGHT)
        logoRect = logo.get_rect()
        logoRect.center = get.CENTRE
        screen.blit(logo, logoRect)

        # play button -> move to play screen
        x = get.X25 - get.BUTTON_DEFAULT_WIDTH // 2
        y = int(get.WINHEIGHT * get.HOME_BUTTON_Y_REL - get.BUTTON_DEFAULT_HEIGHT // 2)
        play_button = Button(text="PLAY", x=x, y=y, click_pos=click_pos)
        screen.blit(play_button.surface, (x, y))

        # set button -> move to settings screen
        x = get.X50 - get.BUTTON_DEFAULT_WIDTH
        settings_button = Button(text="SETTINGS", x=x, y=y, width=int(get.BUTTON_DEFAULT_WIDTH * 2), click_pos=click_pos)
        screen.blit(settings_button.surface, (x, y))

        # quit button -> exit the game
        x = get.X75 - get.BUTTON_DEFAULT_WIDTH // 2
        quit_button = Button(text="QUIT", x=x, y=y, click_pos=click_pos)
        screen.blit(quit_button.surface, (x, y))

        # click actions
        if quit_button.was_clicked(click_pos):
            utils.delay_n_frames()
            _quit_button_action()
        elif play_button.was_clicked(click_pos):
            utils.delay_n_frames()
            _play_button_action()
        elif settings_button.was_clicked(click_pos):
            utils.delay_n_frames()
            _settings_button_action()

    def _render_settings_screen(self, screen, click_pos, key_press):
        """Draw the set screen."""

        def _back_button_action():
            self.game_status = get.STATUS_HOME

        #  background imagery
        screen.fill(get.LOGO_SCREEN_BACKGROUND_COLOR)
        logo = pygame.image.load(get.LOGO_SCREEN_IMAGE_PATH).convert_alpha()
        logo.fill((255, 255, 255, get.SETTINGS_LOGO_IMG_ALPHA), None, pygame.BLEND_RGBA_MULT)
        logo = utils.reshape_keep_aspect(logo, new_height=get.WINHEIGHT * get.LOGO_HEIGHT_RELATIVE_TO_SCREEN_HEIGHT)
        logoRect = logo.get_rect()
        logoRect.center = get.CENTRE
        screen.blit(logo, logoRect)

        # buttons
        # back button -> move to home screen
        x = get.X25 - get.BUTTON_DEFAULT_WIDTH // 2
        y = int(get.WINHEIGHT * get.HOME_BUTTON_Y_REL - get.BUTTON_DEFAULT_HEIGHT // 2)
        back_button = Button(text="BACK", x=x, y=y, click_pos=click_pos)
        screen.blit(back_button.surface, (x, y))

        # option toggles
        # AI difficulty
        font = pygame.font.Font(get.BUTTON_DEFAULT_FONTNAME, get.BUTTON_DEFAULT_FONTSIZE)
        text = font.render("AI Difficulty", True, get.CREDIT_SCREEN_TEXT_COLOUR)
        textRect = text.get_rect()
        textRect.right = get.X25
        textRect.top = get.Y75
        screen.blit(text, textRect)
        # easy toggleable -> store a setting
        easy_button = Button(text="EASY", x=get.X25, y=get.Y75, width=int(get.BUTTON_DEFAULT_WIDTH * 2), click_pos=click_pos, toggleable=True)
        screen.blit(easy_button.surface, (x, y))

        # click actions
        if back_button.was_clicked(click_pos):
            utils.delay_n_frames()
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
            if self.outro_counter < get.CLOCKSPEED * get.LOGO_DURATION:
                # Logo only
                screen.fill(get.LOGO_SCREEN_BACKGROUND_COLOR)
                logo = pygame.image.load(get.LOGO_SCREEN_IMAGE_PATH).convert_alpha()
                logo = utils.reshape_keep_aspect(logo, new_height=get.WINHEIGHT * get.LOGO_HEIGHT_RELATIVE_TO_SCREEN_HEIGHT)
                logoRect = logo.get_rect()
                logoRect.center = get.CENTRE
                screen.blit(logo, logoRect)
                self.outro_counter += 1
            else:
                # else the title sequence must end
                self.outro_sequence_position += 1
                self.outro_counter = 0

        # else if we are on the developer credit
        elif self.outro_sequence_position == 2:
            if self.outro_counter < get.CLOCKSPEED * get.OUTRO_DURATION:
                screen.fill(get.OUTRO_SCREEN_BACKGROUND_COLOR)
                # first line
                font1 = pygame.font.Font(get.OUTRO_SCREEN_FONT, get.OUTRO_SCREEN_FONT_SIZE1)
                text1 = font1.render(get.OUTRO_SCREEN_TEXT1, True, get.OUTRO_SCREEN_TEXT_COLOUR)
                textRect1 = text1.get_rect()
                textRect1.center = (get.X50, get.Y75)
                screen.blit(text1, textRect1)

                # second line
                font2 = pygame.font.Font(get.OUTRO_SCREEN_FONT, get.OUTRO_SCREEN_FONT_SIZE2)
                text2 = font2.render(get.OUTRO_SCREEN_TEXT2, True, get.OUTRO_SCREEN_TEXT_COLOUR)
                textRect2 = text2.get_rect()
                textRect2.center = (get.X50, get.Y50)
                screen.blit(text2, textRect2)

                # third line
                font3 = pygame.font.Font(get.OUTRO_SCREEN_FONT, get.OUTRO_SCREEN_FONT_SIZE3)
                text3 = font3.render(get.OUTRO_SCREEN_TEXT3, True, get.OUTRO_SCREEN_TEXT_COLOUR)
                textRect3 = text3.get_rect()
                textRect3.center = (get.X50, get.Y25)
                screen.blit(text3, textRect3)

                self.outro_counter += 1

            else:
                pygame.quit()
                sys.exit()

    def _render_play_mode(self, screen, click_pos, key_press):
        """Draw the play screen."""

        def _back_button_action():
            self.game_status = get.STATUS_HOME
            print("back clicked")

        #  background imagery
        screen.fill(get.LOGO_SCREEN_BACKGROUND_COLOR)
        logo = pygame.image.load(get.LOGO_SCREEN_IMAGE_PATH).convert_alpha()
        logo.fill((255, 255, 255, get.SETTINGS_LOGO_IMG_ALPHA), None, pygame.BLEND_RGBA_MULT)
        logo = utils.reshape_keep_aspect(logo, new_height=get.WINHEIGHT * get.LOGO_HEIGHT_RELATIVE_TO_SCREEN_HEIGHT)
        logoRect = logo.get_rect()
        logoRect.center = get.CENTRE
        screen.blit(logo, logoRect)

        # buttons
        # back button -> move to home screen
        x = get.X25 - get.BUTTON_DEFAULT_WIDTH // 2
        y = int(get.WINHEIGHT * get.HOME_BUTTON_Y_REL - get.BUTTON_DEFAULT_HEIGHT // 2)
        back_button = Button(text="BACK", x=x, y=y, click_pos=click_pos)
        screen.blit(back_button.surface, (x, y))
        # start game button -> move to main game loop
        x = get.X50 - get.BUTTON_DEFAULT_WIDTH // 2
        y = int(get.WINHEIGHT * get.HOME_BUTTON_Y_REL - get.BUTTON_DEFAULT_HEIGHT // 2)
        back_button = Button(text="BACK", x=x, y=y, click_pos=click_pos)
        screen.blit(back_button.surface, (x, y))

        # click actions
        if back_button.was_clicked(click_pos):
            utils.delay_n_frames()
            _back_button_action()
