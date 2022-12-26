"""
The main Game class.

This controls all the sequences of the game and deals with their rendering.
"""
import logging
from random import randint
import sys
import textwrap

import pygame

import cryptids.settings as get
from cryptids import utils
from cryptids.button import Button
from cryptids import usermanagement
from cryptids import gameplay

# get the logger
logger = logging.getLogger(__name__)
if get.VERBOSE:
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
        self.login_success = False
        self.game_started = False
        self.username = None
        self.user = None
        self.username_text = get.DEFAULT_USERNAME
        self.password_text = get.DEFAULT_PASSWORD

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
            case get.STATUS_POPUP:
                self._render_status_menu
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

        # settings button -> move to settings screen
        x = get.X50 - get.BUTTON_DEFAULT_WIDTH // 2
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
            if self.login_success:
                self.game_status = get.STATUS_GAMEPLAY
            else:
                logger.info("PRE-PLAY SCREEN: Start button pressed without sucessful login")
                self._render_popup(screen, click_pos, key_press, click_event, "Warning", "Cannot start the game without logging in. This is because we must be able to access your deck. Make an account and register your NFTs or log in to play.")

                pass

        def _login_button_action():
            logger.info("PRE-PLAY SCREEN: login button pressed.")
            # check login
            (return_code, user) = usermanagement.load_user(self.username_text, self.password_text)
            match return_code:
                case 0:
                    self.login_success = True
                    self.username = self.username_text
                    self.user = user
                case 1:
                    logger.info("PRE-PLAY SCREEN: Login attempted but unrecognised username")
                    self._render_popup(screen, click_pos, key_press, click_event, "Warning", "Unrecognised username")
                case 2:
                    logger.info("PRE-PLAY SCREEN: Login attempted but incorrect password")
                    self._render_popup(screen, click_pos, key_press, click_event, "Warning", "Incorrect password")

        def _logout_button_action():
            logger.info("PRE-PLAY SCREEN: logout button pressed.")
            self.login_success = False
            self.username = None
            self.password_text = get.DEFAULT_PASSWORD

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
        start_button = Button(text="START", x=x, y=y, click_pos=click_pos, click_event=click_event, access=self.login_success)
        screen.blit(start_button.surface, (x, y))

        if self.login_success:
            # LOGGED IN SCREEN

            # login button -> move to main game loop
            x = get.X50 - get.BUTTON_DEFAULT_WIDTH // 2
            y = int(get.WINHEIGHT * get.HOME_BUTTON_Y_REL - get.BUTTON_DEFAULT_HEIGHT // 2)
            log_button = Button(text="LOG OUT", x=x, y=y, click_pos=click_pos, click_event=click_event)
            screen.blit(log_button.surface, (x, y))

            x = 0
            y = 0
            logged_in_user_status = Button(text=f"Logged in as {self.username}.", x=x, y=y, click_pos=click_pos, click_event=click_event, access=False, width=get.WINWIDTH // 5, height=get.WINHEIGHT // 20, font_colour=get.RED)
            screen.blit(logged_in_user_status.surface, (x, y))

            # !!! pick deck
            self.user_deck_selection = utils.str_to_list(usermanagement.get_setting(self.user, "settings", "loadouts", "default"))
            # user settings
        else:
            # logout button -> move to main game loop
            x = get.X50 - get.BUTTON_DEFAULT_WIDTH // 2
            y = get.Y25
            log_button = Button(text="LOG IN", x=x, y=y, click_pos=click_pos, click_event=click_event)
            screen.blit(log_button.surface, (x, y))

            # login text boxes
            font = pygame.font.Font(get.PREPLAY_LOGIN_TEXT_FONT, get.PREPLAY_LOGIN_TEXT_FONTSIZE)
            text = font.render("USERNAME:", True, get.PREPLAY_LOGIN_TEXT_COLOUR)
            textRect = text.get_rect()
            textRect.left = get.X25
            textRect.top = get.Y50 - 25
            screen.blit(text, textRect)
            x, y = get.X50, get.Y50 - 25
            username_textbox = Button(x=x, y=y, click_pos=click_pos, click_event=click_event, input_text=True, text=self.username_text)
            screen.blit(username_textbox.surface, (x, y))

            font = pygame.font.Font(get.PREPLAY_LOGIN_TEXT_FONT, get.PREPLAY_LOGIN_TEXT_FONTSIZE)
            text = font.render("PASSWORD:", True, get.PREPLAY_LOGIN_TEXT_COLOUR)
            textRect = text.get_rect()
            textRect.left = get.X25
            textRect.top = get.Y50 + 25
            x, y = get.X50, get.Y50 + 25
            password_textbox = Button(x=x, y=y, click_pos=click_pos, click_event=click_event, input_text=True, text=self.password_text, private=True)
            screen.blit(password_textbox.surface, (x, y))
            screen.blit(text, textRect)

            # login specific buttons
            if username_textbox.was_clicked(click_pos) and click_event:
                self.username_text = username_textbox.text_input_action(screen)

            if password_textbox.was_clicked(click_pos) and click_event:
                self.password_text = password_textbox.text_input_action(screen)

        # click actions
        if back_button.was_clicked(click_pos) and click_event:
            utils.delay_n_frames(num_frames=get.DEFAULT_BUTTON_DELAY_ON_CLICK * get.CLOCKSPEED, clockspeed=get.CLOCKSPEED)
            _back_button_action()

        if start_button.was_clicked(click_pos) and click_event:
            utils.delay_n_frames(num_frames=get.DEFAULT_BUTTON_DELAY_ON_CLICK * get.CLOCKSPEED, clockspeed=get.CLOCKSPEED)
            _start_button_action()

        if log_button.was_clicked(click_pos) and click_event:
            utils.delay_n_frames(num_frames=get.DEFAULT_BUTTON_DELAY_ON_CLICK * get.CLOCKSPEED, clockspeed=get.CLOCKSPEED)
            if self.login_success:
                # if we are logged in, we need the logout action
                _logout_button_action()
            else:
                # if we are not logged in, we need the login button
                _login_button_action()

        # keyboard actions
        if key_press in get.K_BACK:
            _back_button_action()

    def _render_pause_menu(self, screen, click_pos, key_press, click_event):
        """Draw the pause menu."""
        def _resume_button_action():
            logger.info("PAUSE SCREEN: Resume button pressed.")
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

    def _render_popup(self, screen, click_pos, key_press, click_event, heading, body):
        """Draw a popup."""
        # set the loop break
        ok_pressed = False

        # Set up game clock
        clock = pygame.time.Clock()
        # enter the event loop
        while not ok_pressed:
            events = pygame.event.get()
            # flags
            click_event = False
            # if we have any, process them.
            if events:
                for event in events:

                    # check if the window is closed
                    if event.type == pygame.QUIT:
                        logger.info("Quit event detected. Closing the game.")
                        # if so, end the script by breaking the while loop
                        ok_pressed = True
                        # Quit Pygame
                        pygame.quit()
                        sys.exit()

                    # check if a click event occured
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        click_pos = event.pos
                        click_event = True
                        logger.debug(f"CLICK at {click_pos}")
                    else:
                        click_pos = None

            # make a transparent background
            xoffset = (get.WINWIDTH - get.POPUP_WINWIDTH) // 2
            yoffset = (get.WINHEIGHT - get.POPUP_WINHEIGHT) // 2
            popup = pygame.Surface((get.POPUP_WINWIDTH, get.POPUP_WINHEIGHT))
            popup.fill(get.POPUP_MENU_BACKGROUND_COLOUR)
            popup.set_alpha(get.POPUP_MENU_BACKGROUND_TRANSPARENCY)
            # pull up the logo
            logo = pygame.image.load(get.LOGO_SCREEN_IMAGE_PATH).convert_alpha()
            logo.fill((255, 255, 255, get.SETTINGS_LOGO_IMG_ALPHA), None, pygame.BLEND_RGBA_MULT)
            logo = utils.reshape_keep_aspect(logo, new_height=get.POPUP_WINHEIGHT * get.LOGO_HEIGHT_RELATIVE_TO_SCREEN_HEIGHT)
            logoRect = logo.get_rect()
            logoRect.center = get.POPUP_CENTRE
            popup.blit(logo, logoRect)

            # heading text
            font = pygame.font.Font(get.POPUP_SCREEN_POPUP_HEADING_FONT, get.POPUP_SCREEN_POPUP_HEADING_FONTSIZE)
            head = font.render(heading.upper(), True, get.POPUP_SCREEN_POPUP_HEADING_COLOUR)
            headingRect = head.get_rect()
            headingRect.center = (get.POPUP_X50, get.POPUP_HEADING_Y)
            popup.blit(head, headingRect)

            # body text
            font = pygame.font.Font(get.POPUP_SCREEN_POPUP_BODY_FONT, get.POPUP_SCREEN_POPUP_BODY_FONTSIZE)
            # wrap the text
            pixel_width = get.POPUP_WINWIDTH - get.POPUP_BODY_TEXT_OFFSET
            char_width = get.POPUP_SCREEN_POPUP_BODY_FONTSIZE * 0.8
            lines = textwrap.wrap(body.upper(), width=pixel_width // char_width)
            # make a surface per line
            line_surfaces = []
            for line in lines:
                line_surfaces.append(font.render(line, True, get.POPUP_SCREEN_POPUP_BODY_COLOUR))
            # find the box dimensions
            box_width = max(line_surface.get_width() for line_surface in line_surfaces)
            box_height = sum(line_surface.get_height() for line_surface in line_surfaces)
            # build the text box
            text_box = pygame.Surface((box_width, box_height))
            # render the lines to the text box
            y_offset = 0
            for line_surface in line_surfaces:
                text_box.blit(line_surface, (0, y_offset))
                y_offset += line_surface.get_height()
            # render the textbox to the popup
            textRect = text_box.get_rect()
            textRect.center = get.POPUP_CENTRE
            popup.blit(text_box, textRect)

            # ok button -> return to previous state
            x = get.X50 - get.BUTTON_DEFAULT_WIDTH // 2
            y = get.POPUP_WINHEIGHT - get.POPUP_BODY_TEXT_OFFSET
            ok_button = Button(text="OK", x=x, y=y, click_pos=click_pos, click_event=click_event, width=get.BUTTON_DEFAULT_WIDTH)

            screen.blit(popup, (xoffset, yoffset))
            screen.blit(ok_button.surface, (x, y))

            # click actions
            if ok_button.was_clicked(click_pos) and click_event:
                utils.delay_n_frames(num_frames=get.DEFAULT_BUTTON_DELAY_ON_CLICK * get.CLOCKSPEED, clockspeed=get.CLOCKSPEED)
                ok_pressed = True

            # tick the clock
            clock.tick(get.CLOCKSPEED)
            # Update the display
            pygame.display.update()

    def _render_gameplay(self, screen, click_pos, key_press, click_event):
        """Draw gameplay."""
        def _menu_button_action():
            logger.info("GAMEPLAY SCREEN: Menu button pressed.")
            self.game_status = get.STATUS_PAUSE

        # costly initialisations, only desire to do this ONCE at start of game.
        if not self.game_started:
            # initialise the players
            # !!! render a loading screen.
            self.player1 = gameplay.Player(self.username, self.user, self.user_deck_selection)
            self.opponent = gameplay.PlayerAI()

            # build the game board
            self.gameboard = gameplay.GameBoard()

            # update game started status.
            self.game_started = True

        # process new changes
        x, y = pygame.mouse.get_pos()
        if key_press is not None:
            pass

        # keyboard actions
        # get pause menu
        if key_press in get.K_ESC:
            _menu_button_action()
