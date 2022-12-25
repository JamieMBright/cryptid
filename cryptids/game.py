"""
The main Game class.

This controls all the sequences of the game and deals with their rendering.
"""
import logging
import sys
from random import randint

import pygame

import cryptids.settings as get
from cryptids import utils
from cryptids.button import Button

# get the logger
logger = logging.getLogger(__name__)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


class GameWrapper(object):
    """Wrapper that renders the game."""

    def __init__(self, status: str = get.DEFAULT_STATUS):
        self.game_status = status
        self.intro_sequence_position = 1
        self.outro_sequence_position = 1
        self.intro_counter = 0
        self.outro_counter = 0
        self.focus_pos = [0, 0]
        self.letters = []
        self.fresh_screen = True

    def render(self, screen, click_pos, key_press, click_event: bool) -> object:
        """Select the game status to render."""
        match self.game_status:
            case get.STATUS_INTRO:
                self._render_intro(screen, click_pos, key_press, click_event)
            case get.STATUS_HOME:
                self._render_home_screen(screen, click_pos, key_press, click_event)
            case get.STATUS_SETTINGS:
                self._render_settings_screen(screen, click_pos, key_press, click_event)
            case get.STATUS_PREPLAY:
                self._render_pre_play_mode(screen, click_pos, key_press, click_event)
            case get.STATUS_OUTRO:
                self._render_outro(screen, click_pos, key_press, click_event)
            case get.STATUS_GAMEPLAY:
                self._render_gameplay(screen, click_pos, key_press, click_event)
            case get.STATUS_PAUSE:
                self._render_pause_menu(screen, click_pos, key_press, click_event)
            case _:
                raise ValueError(f"Unrecognised game_status: {self.game_status}")
        return self

    def _render_intro(self, screen, click_pos, key_press, click_event):
        """
        "Draw the intro.

        The intro has three sequences:

            sequence 1) Cryptids title text appears
            sequence 2) Developer credit
            sequence 3) Cryptid logo

        """
        # if we are in the title screen
        match self.intro_sequence_position:
            case 1:
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
                    logger.info("Moving to the title screen.")
                    self.intro_sequence_position += 1
                    self.intro_counter = 0

        # else if we are on the developer credit
            case 2:
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
                    logger.info("Moving to logo screen.")
                    self.intro_sequence_position += 1
                    self.intro_counter = 0

        # else if we are on the logo screen.
            case 3:
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
                    logger.info("Moving to home screen.")
                    self.game_status = get.STATUS_HOME
        return self

    def _render_home_screen(self, screen, click_pos, key_press, click_event):
        """Draw the home screen."""
        def _quit_button_action():
            logger.info("HOME SCREEN: Quit button pressed.")
            self.game_status = get.STATUS_OUTRO

        def _play_button_action():
            logger.info("HOME SCREEN: Play button pressed.")
            self.game_status = get.STATUS_PREPLAY

        def _settings_button_action():
            logger.info("HOME SCREEN: Settings button pressed.")
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
        play_button = Button(text="PLAY", x=x, y=y, click_pos=click_pos, click_event=click_event)
        screen.blit(play_button.surface, (x, y))

        # set button -> move to settings screen
        x = get.X50 - get.BUTTON_DEFAULT_WIDTH
        settings_button = Button(text="SETTINGS", x=x, y=y, click_pos=click_pos, click_event=click_event)
        screen.blit(settings_button.surface, (x, y))

        # quit button -> exit the game
        x = get.X75 - get.BUTTON_DEFAULT_WIDTH // 2
        quit_button = Button(text="QUIT", x=x, y=y, click_pos=click_pos, click_event=click_event)
        screen.blit(quit_button.surface, (x, y))

        # click actions
        if quit_button.was_clicked(click_pos) and click_event:
            utils.delay_n_frames(num_frames=get.DEFAULT_BUTTON_DELAY_ON_CLICK * get.CLOCKSPEED, clockspeed=get.CLOCKSPEED)
            _quit_button_action()
        elif play_button.was_clicked(click_pos) and click_event:
            utils.delay_n_frames(num_frames=get.DEFAULT_BUTTON_DELAY_ON_CLICK * get.CLOCKSPEED, clockspeed=get.CLOCKSPEED)
            _play_button_action()
        elif settings_button.was_clicked(click_pos) and click_event:
            utils.delay_n_frames(num_frames=get.DEFAULT_BUTTON_DELAY_ON_CLICK * get.CLOCKSPEED, clockspeed=get.CLOCKSPEED)
            _settings_button_action()
        # keyboard actions
        if key_press in get.K_BACK:
            pass
        if key_press in get.K_ESC:
            _quit_button_action()

    def _render_settings_screen(self, screen, click_pos, key_press, click_event):
        """Draw the set screen."""
        def _back_button_action():
            logger.info("SETTINGS SCREEN: Back button pressed.")
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
        back_button = Button(text="BACK", x=x, y=y, click_pos=click_pos, click_event=click_event)
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
        x, y = get.X50, get.Y50
        easy_button = Button(text="EASY", x=x, y=y, click_pos=click_pos, toggleable=True, click_event=click_event)
        screen.blit(easy_button.surface, (x, y))

        # click actions
        if back_button.was_clicked(click_pos) and click_event:
            utils.delay_n_frames(num_frames=get.DEFAULT_BUTTON_DELAY_ON_CLICK * get.CLOCKSPEED, clockspeed=get.CLOCKSPEED)
            _back_button_action()
        # keyboard actions
        if key_press in get.K_BACK:
            _back_button_action()

    def _render_outro(self, screen, click_pos, key_press, click_event):
        """
        "Draw the outtro.

        The outro has two sequence:

            sequence 1) Cryptid logo
            sequence 2) Thank you + credit

        """
        # if we are in the title screen
        match self.outro_sequence_position:
            case 1:
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
                    logging.info("moving to thanks scren.")
                    self.outro_sequence_position += 1
                    self.outro_counter = 0

            # else if we are on the developer credit
            case 2:
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
                    logging.info("exiting")
                    self.outro_sequence_position += 1
                    self.outro_counter

            case 3:
                pygame.quit()
                sys.exit()

    def _render_pre_play_mode(self, screen, click_pos, key_press, click_event):
        """Draw the play screen."""

        def _back_button_action():
            logger.info("PRE-PLAY SCREEN: Back button pressed.")
            self.game_status = get.STATUS_HOME

        def _start_button_action():
            logger.info("PRE-PLAY SCREEN: Start button pressed.")
            self.game_status = get.STATUS_GAMEPLAY

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
        back_button = Button(text="BACK", x=x, y=y, click_pos=click_pos, click_event=click_event)
        screen.blit(back_button.surface, (x, y))
        # start game button -> move to main game loop
        x = get.X75 - get.BUTTON_DEFAULT_WIDTH // 2
        y = int(get.WINHEIGHT * get.HOME_BUTTON_Y_REL - get.BUTTON_DEFAULT_HEIGHT // 2)
        start_button = Button(text="START", x=x, y=y, click_pos=click_pos, click_event=click_event)
        screen.blit(start_button.surface, (x, y))

        # click actions
        if back_button.was_clicked(click_pos) and click_event:
            utils.delay_n_frames(num_frames=get.DEFAULT_BUTTON_DELAY_ON_CLICK * get.CLOCKSPEED, clockspeed=get.CLOCKSPEED)
            _back_button_action()

        if start_button.was_clicked(click_pos) and click_event:
            utils.delay_n_frames(num_frames=get.DEFAULT_BUTTON_DELAY_ON_CLICK * get.CLOCKSPEED, clockspeed=get.CLOCKSPEED)
            _start_button_action()

        # keyboard actions
        if key_press in get.K_BACK:
            _back_button_action()

    def _render_gameplay(self, screen, click_pos, key_press, click_event):
        """Draw gameplay."""
        def _menu_button_action():
            logger.info("GAMEPLAY SCREEN: Menu button pressed.")
            self.game_status = get.STATUS_PAUSE

        # THIS IS THE GAME
        # draw background
        if self.fresh_screen:
            self._fresh_game_screen(screen)

            # process new changes
        x, y = pygame.mouse.get_pos()
        if key_press is not None:
            # translate the latter to screen
            rand_colour = (randint(0, 255), randint(0, 255), randint(0, 255))
            font = pygame.font.Font(get.GAME_FONT, get.GAME_FONT_SIZE)
            letter = Letter(x, y, rand_colour, font, key_press)
            self.letters.append(letter)
            logger.debug(f"letter with message {letter.msg} of colour {letter.col}")
            letter.draw(screen)

        # keyboard actions
        # get pause menu
        if key_press in get.K_ESC:
            _menu_button_action()

    def _fresh_game_screen(self, screen):
        logger.info("Fresh game screen requested.")
        background(screen)
        for letter in self.letters:
            letter.draw(screen)
        self.fresh_screen = False

    def _render_pause_menu(self, screen, click_pos, key_press, click_event):
        """Draw the pause menu."""
        def _resume_button_action():
            logger.info("PAUSE SCREEN: Resume button pressed.")
            self.fresh_screen = True
            self.game_status = get.STATUS_GAMEPLAY

        def _quit_button_action():
            logger.info("PAUSE SCREEN: Quit button pressed.")
            self.game_status = get.STATUS_HOME

        # make a transparent background
        xoffset = (get.WINWIDTH - get.PAUSE_WINWIDTH) // 2
        yoffset = (get.WINHEIGHT - get.PAUSE_WINHEIGHT) // 2
        menu = pygame.Surface((get.PAUSE_WINWIDTH, get.PAUSE_WINHEIGHT))
        menu.fill(get.PAUSE_MENU_BACKGROUND_COLOUR)
        menu.set_alpha(get.PAUSE_MENU_BACKGROUND_TRANSPARENCY)
        # pull up the logo
        logo = pygame.image.load(get.LOGO_SCREEN_IMAGE_PATH).convert_alpha()
        logo.fill((255, 255, 255, get.SETTINGS_LOGO_IMG_ALPHA), None, pygame.BLEND_RGBA_MULT)
        logo = utils.reshape_keep_aspect(logo, new_height=get.PAUSE_WINHEIGHT * get.LOGO_HEIGHT_RELATIVE_TO_SCREEN_HEIGHT)
        logoRect = logo.get_rect()
        logoRect.center = get.PAUSE_CENTRE
        menu.blit(logo, logoRect)
        screen.blit(menu, (xoffset, yoffset))

        # pause text
        font = pygame.font.Font(get.PAUSE_SCREEN_PAUSE_TEXT_FONT, get.PAUSE_SCREEN_PAUSE_TEXT_FONTSIZE)
        text = font.render("PAUSED", True, get.PAUSE_SCREEN_PAUSE_TEXT_COLOUR)
        textRect = text.get_rect()
        textRect.center = (get.X50, get.Y50)
        screen.blit(text, textRect)

        # resume button -> return to game
        x = get.PAUSE_X25 - get.BUTTON_DEFAULT_WIDTH // 2
        y = get.PAUSE_Y75
        resume_button = Button(text="RESUME", x=x, y=y, click_pos=click_pos, click_event=click_event)
        screen.blit(resume_button.surface, (x, y))

        # quit button -> exit the game
        x = get.PAUSE_X75 - get.BUTTON_DEFAULT_WIDTH // 2
        y = get.PAUSE_Y75
        quit_button = Button(text="QUIT", x=x, y=y, click_pos=click_pos, click_event=click_event)
        screen.blit(quit_button.surface, (x, y))

        # click actions
        if resume_button.was_clicked(click_pos) and click_event:
            utils.delay_n_frames(num_frames=get.DEFAULT_BUTTON_DELAY_ON_CLICK * get.CLOCKSPEED, clockspeed=get.CLOCKSPEED)
            _resume_button_action()

        if quit_button.was_clicked(click_pos) and click_event:
            utils.delay_n_frames(num_frames=get.DEFAULT_BUTTON_DELAY_ON_CLICK * get.CLOCKSPEED, clockspeed=get.CLOCKSPEED)
            _quit_button_action()


def background(screen):
    """Draw the background."""
    screen.fill("Black")


class Letter(object):
    """A letter for testing a game."""

    def __init__(self, x, y, col, font, msg):
        self.x = x
        self.y = y
        self.col = col
        self.font = font
        self.msg = msg
        self.textobj = font.render(msg, True, col)

    def draw(self, screen):
        """Draw the letter."""
        textRect = self.textobj.get_rect()
        textRect.center = (self.x, self.y)
        screen.blit(self.textobj, textRect)

    def __repr__(self):
        """Letter object when printed."""
        return f"LETTER: {self.msg}, COL: {self.col}"
