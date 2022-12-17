import pygame


class Card:
    """
    The Card class.
    """

    def __init__(self, name, card_type, attribute, level, attack, defense, effect_type, effect_description):
        self.name = name
        self.card_type = card_type
        self.attribute = attribute
        self.level = level
        self.attack = attack
        self.defense = defense
        self.effect_type = effect_type
        self.effect_description = effect_description

    def render(self, surface, x, y):
        """
        Render the Card.

        Parameters
        ----------
        surface : TYPE
            DESCRIPTION.
        x : TYPE
            DESCRIPTION.
        y : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        # Load the card image
        image = pygame.image.load("card_images/" + self.name + ".png")

        # Create a font for the card text
        font = pygame.font.Font(None, 24)

        # Render the card name and type
        name_text = font.render(self.name, 1, (0, 0, 0))
        type_text = font.render(self.card_type, 1, (0, 0, 0))

        # Blit the card image and text onto the surface
        surface.blit(image, (x, y))
        surface.blit(name_text, (x + 10, y + 10))
        surface.blit(type_text, (x + 10, y + 30))
