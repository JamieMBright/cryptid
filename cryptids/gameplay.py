"""Gameplay event loop."""
import logging
import random
import sys
from typing import List, Tuple

import pygame

import cryptids.settings as get
from cryptids import usermanagement
from cryptids.utils import check_type
from cryptids.card import Card

logger = logging.getLogger(__name__)
if get.VERBOSE:
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)


class GameBoard(object):
    """
    The GameBoard class.

    The Boardgame class knows where all the cards are, and deals with rendering
    the game assets and visuals. It also has awareness of the focus of the
    player.
    """

    def __init__(self):
        logger.info("Building the GameBoard")
        pass

    def render(self, screen, player1, player2):
        """Render the whole screen."""
        self._render_background(screen)
        self._render_gui(screen, player1, player2)
        self._render_cards_in_play(screen, player1.field, player2.field)
        self._render_highlighted_card(screen, player1)

    def _render_background(self, screen):
        """Draw the background."""
        screen.fill(get.GAME_BOARD_BACKGROUND_COLOUR)

    def _render_gui(self, screen, player1, player2):
        """Draw all the components of the game."""
        # draw the grid
        x, y, w, h = 10, 10, 50, 30
        self.draw_rect(screen, x, y, w, h)

        # draw the health bars
        p1_hp = player1.get_hp()
        p2_hp = player2.get_hp()
        # draw num of cards left
        p1_n_cards_in_deck = player1.get_cards_in_deck()
        p2_n_cards_in_deck = player1.get_cards_in_deck()
        # draw the decks
        if p1_n_cards_in_deck > 0:
            pass  # !!! need to draw this

        # draw the discard piles
        p1_n_cards_in_discard = player1.get_cards_in_discard()
        p2_n_cards_in_discard = player2.get_cards_in_discard()

        # draw the buttons
        pass

    def _render_cards_in_play(self, screen, player):
        """Draw all cards that are in play."""
        pass

    def _render_highlighted_card(self, screen, player):
        """Draw the highlighted card."""
        pass

    @classmethod
    def draw_rect(screen: pygame.Surface,
                  x: int,
                  y: int,
                  width_abs: int = None,
                  height_abs: int = None,
                  width_rel: (int, float) = None,
                  height_rel: (int, float) = None,
                  border_thickness: int = get.GRID_BORDER_THICKNESS,
                  border_colour: (str, Tuple[int, int, int]) = get.GRID_BORDER_DEFAULT_COLOUR):
        """Draw a transparent rectangle."""
        # checks
        check_type(screen, "screen", pygame.Surface)
        check_type(x, "x", int)
        check_type(y, "y", int)
        if width_abs is not None:
            check_type(width_abs, "width_abs", int)
        if width_rel is not None:
            check_type(width_rel, "width_rel", int)
        if height_abs is not None:
            check_type(height_abs, "height_abs", int)
        if height_rel is not None:
            check_type(height_rel, "height_rel", int)
        check_type(border_thickness, "border_thickness", int)
        check_type(border_colour, "border_colour", (str, Tuple[int, int, int]))
        if width_abs is not None and width_rel is not None:
            raise ValueError("Both absolute and relative widths were provided. Can only provide one.")
        elif width_abs is None and width_rel is None:
            raise TypeError("Need at least one width, abs or rel")
        if height_abs is not None and height_rel is not None:
            raise ValueError("Both absolute and relative heights were provided. Can only provide one.")
        elif height_abs is None and height_rel is None:
            raise TypeError("Need at least one height, abs or rel")

        # get the widths and heights
        W = get.WINWIDTH
        H = get.WINHEIGHT

        if width_abs is not None:
            width = width_abs
        elif width_rel is not None:
            width = int(W * width_rel)

        if height_abs is not None:
            height = height_abs
        elif height_rel is not None:
            height = int(H * height_rel)

        # Draw the rectangle)
        return pygame.draw.rect(screen, border_colour, (x, y, width, height), border_thickness)


class Player(usermanagement.User):
    """The Player class."""

    def __init__(self,
                 username,
                 user,
                 user_deck_selection: List[int]):
        """
        Build the player class.

        Parameters
        ----------
        username : TYPE
            DESCRIPTION.
        user : TYPE
            DESCRIPTION.
        user_deck_selection : List[int]
            DESCRIPTION.

        Returns
        -------
        None.

        Testing
        -------
        username = "default"
        user = {'email': 'waimanu@cryptids-tcg.com', 'password': 'Password123', 'settings': {'nfts': [0], 'loadouts': {'default': '[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50]'}}, 'records': {'wins': 0, 'losses': 0}}
        user_deck_selection = [x + 1 for x in range(get.DECK_SIZE)]
        self = Player(username, user, user_deck_selection)
        self.hand
        """
        # initialize the User variable
        super().__init__(username, user)
        # objects loaded: self.loadouts, self.nfts

        logger.info(f"Building the Player for {username}.")
        # initialize specifics
        self.user_deck_selection = user_deck_selection
        # card locations
        self._load_deck()  # instantiates self.deck
        self.discard = []
        self.hand = []
        self.magic = []
        self.fill_hand()  # fills the hand with cards from the deck
        self.field = {}  # !!! OrderedDict?
        for i in range(get.FIELD_SIZE):
            self.field[i] = None
        self.hp_starting = get.STARTING_HP
        self.hp_current = get.STARTING_HP
        self.deck_size = get.DECK_SIZE
        self.hand_size = get.HAND_SIZE
        self.dead_value = 0  # !!! fun mechanic/spell to have negative life?
        self.dead = False
        self.turn = 0
        self.end_turn()  # end the turn to update all card statuses

    def __repr__(self):
        """Print to screen when called."""
        msg = f"""----------------------
PLAYER:    {self.username}
HP:   {self.hp_current} / {self.hp_starting}
TURN:      {self.turn}
----------------------
DECK       ({self.get_cards_in_deck()}/{self.deck_size})
HAND       ({self.get_cards_in_hand()}/{self.hand_size})
DISCARD    ({self.get_cards_in_discard()}/{self.deck_size})
MAGIC      ({self.get_n_magic_cards_in_play()})
FIELD      ({self.get_n_cryptids_on_field()}/{get.FIELD_SIZE})
----------------------
"""
        for i in range(get.FIELD_SIZE):
            msg += f"""FIELD POSITION {i} = {'card ' + str(self.field[i].card_id) + " " + str(self.field[i].name) if self.field[i] is not None else 'empty'}\n"""
        return msg

    def _load_deck(self) -> None:
        """Get the deck of the player."""
        # Initialize the cards that the user has selected and place them in the deck
        self.deck = [Card(card_id).set_location("deck") for card_id in self.user_deck_selection]
        # shuffle the deck
        random.shuffle(self.deck)
        logger.info(f"{self.username}'s deck loaded and shuffled.")

    def fill_hand(self) -> None:
        """Fill the hand with minimum number of cards."""
        logger.info("Filling the hand with min allowable cards.")
        while self.get_cards_in_hand() < get.HAND_SIZE:
            if self.get_cards_in_deck() > 0:
                self.draw_card_to_hand()

    def is_dead(self):
        """Return if the player is dead."""
        return self.dead

    def get_cards_in_deck(self) -> int:
        """Return the number of cards left in the player's deck."""
        if self.deck is None:  # if the list is empty
            return 0
        else:
            return len(self.deck)

    def get_cards_in_hand(self) -> int:
        """Return the number of cards left in the player's hand."""
        if not self.hand:  # if the list is empty
            return 0
        else:
            return len(self.hand)

    def get_cards_in_discard(self) -> int:
        """Return the number of cards left in the player's deck."""
        if not self.discard:  # if the list is empty
            return 0
        else:
            return len(self.discard)

    def get_n_cryptids_on_field(self) -> int:
        """Return the number of cryptids in play."""
        count = 0
        for key in range(get.FIELD_SIZE):
            if self.field[key] is not None:
                count += 1
        return count

    def get_n_magic_cards_in_play(self) -> int:
        """Return the number of magic cards in play."""
        if not self.magic:  # if the list is empty
            return 0
        else:
            return len(self.magic)

    def draw_card_to_hand(self) -> None:
        """Draw a card from deck to destination."""
        if self.get_cards_in_deck() > 0:
            logger.info(f"{self.username}'s drawing card.")
            self.hand.append(self.deck.pop().set_location("hand"))
        else:
            logger.fatal("No cards left in deck.")
            raise ValueError("No cards left in deck.")

    def draw_card_to_discard(self) -> None:
        """Draw a card from deck to destination."""
        if self.get_cards_in_deck() > 0:
            logger.info(f"{self.username}'s drawing card.")
            self.discard.append(self.deck.pop().set_location("discard"))
        else:
            logger.fatal("No cards left in deck.")
            raise ValueError("No cards left in deck.")

    def summon_card(self, origin, card_pos, field_pos) -> List[Card]:
        """Play cryptid card from origin list to field."""
        logger.info(f"Summoning crypotid Card {origin[card_pos].card_id} to field position {field_pos}.")
        # check there is no cryptid already in the position
        if self.field[field_pos] is None:
            # check that the card is a cryptid, not magic
            if origin[card_pos].type == "cryptid":
                # ensure the card is playable
                if origin[card_pos].is_playable():
                    # pop returns the card object. play_card updates the card object
                    # and also returns self. put this card in the field dict.
                    self.field[field_pos] = origin.pop(card_pos).play_card().set_location("field")
                    return origin
                # the below errors should have been handled in gameplay buttons
                # therefore this is a fatal error should the above checks be
                # violated.
                else:
                    logger.fatal("Tried to summon a card that is not summonable.")
                    raise ValueError("Tried to summon a card that is not summonable.")
            else:
                logger.fatal("Tried to summon a magic card")
                raise ValueError("Tried to summon a magic card")
        else:
            logger.fatal(f"Field pos: {field_pos} already contains a card.")
            raise ValueError(f"Field pos: {field_pos} already contains a card.")

    def play_magic_card(self, origin, card_pos) -> List[Card]:
        """Play magic card from origin list to field."""
        logger.info(f"Playing magic Card {origin[card_pos].card_id} to magic active.")
        # check that the card is a cryptid, not magic
        if origin[card_pos].type == "magic":
            # ensure the card is playable
            if origin[card_pos].is_playable():
                # pop returns the card object. play_card updates the card object
                # and also returns self. put this card in the field dict.
                self.magic_ = origin.pop(card_pos).play_card().set_location("magic")
                return origin
            # the below errors should have been handled in gameplay buttons
            # therefore this is a fatal error should the above checks be
            # violated.
            else:
                logger.fatal("Tried to play a card that is not playable.")
                raise ValueError("Tried to summon a card that is not playable.")
        else:
            logger.fatal("Tried to play a cryptid card")
            raise ValueError("Tried to play a cryptid card")

    def discard_card(self, origin: List[Card], pos: int) -> List[Card]:
        """Discard the pos-th position Card from origin."""
        logger.info("Discarding {origin[pos]}")
        self.discard.append(origin.pop(pos).set_location("discard"))
        return origin

    def attack_received(self, dmg: int, field_pos: int = None) -> None:
        """
        Deal damage to a particular cryptid and distribute excess damage.

        The planned mechanic for this is that a singular monster receives the
        full damage of the attack, and any excess is spread to all other
        cryptids. If there are no other cryptids or no cryptids at all, then
        the damage is applied directly to player hp. If the overspill damage
        kills the next cryptid, the overspill does NOT reduce the player HP,
        as the damage was directed away from the player.
        """
        if field_pos is None:
            # attack straight to health
            return self.reduce_hp(dmg)
        # else a specific cryptid is attacked
        # check that a cryptid was selected.
        if self.field[field_pos] is None:
            logger.fatal(f"Field position {field_pos} does not have a cryptid.")
            raise ValueError(f"Field position {field_pos} does not have a cryptid.")
        # deal damage to the card
        excess_damage = self.field[field_pos].receive_damage(dmg)
        # if any excess damage is dealt
        if excess_damage > 0:
            # deal the damage equally to all cryptids.
            n = self.get_n_cryptids_on_field() - 1
            if n == 0:
                return self.reduce_hp(excess_damage)
            else:
                # always want to deal with all damage, but also total ints.
                # to do this, calculate the overspill, and hit first cryptid
                overspill = (excess_damage % n)
                dmg_per_cryptid = (excess_damage - overspill) // n
                for i in get.FIELD_SIZE:
                    if self.field[i] is not None and i != field_pos:
                        self.flield[i].receive_damage(dmg_per_cryptid + overspill)
                        overspill = 0

    def reduce_hp(self, amount: int) -> None:
        """Reduce player's hp by a set amount."""
        self.hp_current -= amount
        # if the hp is depleted, set status to dead.
        if self.hp_current <= self.dead_value:
            self.dead = True

    def end_turn(self):
        """End the turn."""
        # must draw to the minimum number of cards if available in deck.
        self.fill_hand()
        # update cards
        for cards in [self.deck, self.hand, self.discard]:
            for card in cards:
                card.update_on_turn_end(self.turn)
        for i in range(get.FIELD_SIZE):
            if self.field[i] is not None:
                self.field[i].update_on_turn_end(self.turn)
        # update turn number
        self.turn += 1


class PlayerAI(object):
    """My AI Player."""

    def __init__(self):
        """Initialize the AI."""
        logger.info("Building the AI player.")
        self.user_deck_selection = self._random_deck_selection()
        self.deck = self._load_deck()
        self.hp = get.STARTING_HP
        self.deck_size = get.DECK_SIZE
        self.hand_size = get.HAND_SIZE

    def _load_deck(self):
        """Get the deck of the player."""
        # load some player settings
        self.deck = [Card(card_id) for card_id in self.user_deck_selection]

    def _random_deck_selection(self):
        # !!! This should load some preset decks.
        # n = 3
        # start = 0
        # end = 9
        # random_ints = random.sample(range(start, end + 1), n)
        # logger.debug("AI deck selected: {deck}.")
        return [0]
