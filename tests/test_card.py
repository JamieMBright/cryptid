"""
Test cryptids.card
"""
import pytest

from cryptids.card import Card


def test_card():
    """Test the creation of the Card class."""
    card = Card("Blue-Eyes White Dragon", "Monster", "Light", 8, 3000, 2500, "Normal", "")

    assert card.name == "1"
    assert card.card_type == "Monster"
    assert card.attribute == "Light"
    assert card.level == 8
    assert card.attack == 3000
    assert card.defense == 2500
    assert card.effect_type == "Normal"
    assert card.effect_description == ""


def test_render():
    card = Card("1", "Monster", "Light", 8, 3000, 2500, "Normal", "")
    surface = ""
    x, y = 50, 50
    card.render(surface, x, y)
