"""Gameplay event loop."""
from typing import List
import cryptids.settings as get
from cryptids import usermanagement


class GameBoard():
    """
    The GameBoard class.

    The Boardgame class knows where all the cards are, and deals with rendering
    the game assets and visuals. It also has awareness of the focus of the
    player.
    """

    def __init__(self):
        pass

    def render(self):
        """Render the whole screen."""
        self._render_background()
        self._render_gui()
        self._render_cards_in_play()
        self._render_highlighted_card()

    def _render_background(self, screen):
        """Draw the background."""
        screen.fill("Black")

    def _render_gui(self, player):
        """Draw all the components of the game."""
        # draw the health bars
        # draw num of cards left
        # draw the discard piles
        # draw the decks
        # draw the buttons
        pass

    def _render_cards_in_play(self, player):
        """Draw all cards that are in play."""
        pass

    def _render_highlighted_card(self, player):
        """Draw the highlighted card."""
        pass


class Player(usermanagement.User):
    """The Player class."""

    def __init__(self,
                 username,
                 user_deck_selection: List[int]):
        # initialize the User variable
        super().__init__(username)
        # objects loaded: self.loadouts, self.nfts

        # initialize specifics
        self.user_deck_selection = user_deck_selection
        self.deck = self._load_deck()
        self.hp = get.STARTING_HP
        self.deck_size = get.DECK_SIZE
        self.hand_size = get.HAND_SIZE

    def _load_deck(self,):
        """Get the deck of the player."""
        # load some player settings
        self.deck = [Card(card_id) for card_id in self.user_deck_selection]


class PlayerAI(object):
    """My AI Player."""

    def __init__(self, user_deck_selection):
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
        return [0]


class Card(object):
    """Card class."""

    def __init__(self, card_id: int):
        """Initialize the card."""
        self.id = card_id
