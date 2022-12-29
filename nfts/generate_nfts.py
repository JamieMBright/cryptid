"""
Generate the data for NFTs.

Running this script will create a file called nft_info.json and make the nfts
according to the inputs at the start of this script. If data already exists in
the file nft_info.json, then a prompt will be asked to ensure user is aware any
existing data will be overwritten.
"""
import os
import numpy as np
from faker import Faker
from random import randint, random
import pygame
import sys
import traceback
import json

# save data for the NFTs
NFT_FNAME = os.path.join(os.getcwd(), "nfts", "nft_info.json")

# Generate names for the cards
locales = ["en_GB", "de", "es_ES", "fr_FR", "en_IN", "en_IE", "sl_SI", "pl_PL"]
fake = Faker(locales)
fake.name()

# about the cards
TOTAL_UNIQUE_CARDS = 300
# each cryptid has a class. And there must be the same summon level per class.
# e.g., if there is 1 summon level 4, then there must be len(CLASSES) level 4s.
CLASSES = ["gore", "hairy", "cosmic", "undead", "interdimensional", "pleasant"]
# cards per class
cards_per_class = TOTAL_UNIQUE_CARDS // len(CLASSES)
# there are summon levels per card that have a diminising probability of existance
# summon level should also represent rarity, but there needs to be enough so
# that everyone can have them. e.g., a starter deck might include one level 4
SUMMON_LEVELS = np.array([0, 1, 2, 3, 4])
MAGIC_LEVELS = np.array([0, 1, 2])
# what is the break down of the cards available per class. There are magic
# cards of rarity
N_CARDS_PER_X_PER_CLASS = {"magic_level": [7, 2, 1],
                           "summon_level": [25, 10, 4, 1]}
N_CARDS_PER_X_PER_CLASS["all"] = N_CARDS_PER_X_PER_CLASS["magic_level"] + N_CARDS_PER_X_PER_CLASS["summon_level"]

assert cards_per_class == sum(N_CARDS_PER_X_PER_CLASS["all"]), f"Need to reassign the number of cards per sumon level/magic per class. target is {cards_per_class}, but instead have {sum(N_CARDS_PER_X_PER_CLASS['all'])}."

# It is fun if common cards are also rare by scarcity, and some high summon
# levels are common by scarcity. Therefore, rarity is not attached to the total
# number of cards. Simply, there are more summon_level 0 monster variations.
# rarity can therefore be independent of strength.
# a booster pack can therefore be constructed of the number of monsters and
# the number of magic cards. Just because there is a 5% chance to get a levl 4
# summon in this booster pack, rarity dictates which one it might be.
# probabiliy here represents the cumulative sum of probability. e.g. if the
# possible summon level for the card is [2, 3, 4], a probability of [0.6, 0.95]
# means that a random roll <0.6 returns a card of summon2, a rull 0.6<x<0.95
# gives a card of summon 3, and >0.95 gives summon 4.
BOOSTER = {0: {"cryptid": {"summon_level": 0}},
           1: {"cryptid": {"summon_level": 0}},
           2: {"cryptid": {"summon_level": 0}},
           3: {"cryptid": {"summon_level": 0}},
           4: {"cryptid": {"summon_level": [1, 2], "probability": np.array([0.7])}},
           5: {"cryptid": {"summon_level": [2, 3, 4], "probability": np.array([0.6, 0.95])}},
           6: {"magic": {"magic_level": [0, 1, 2], "probability": np.array([0.7, 0.95])}}
           }

cards_per_booster = len(BOOSTER.keys())


def open_booster(booster=BOOSTER,
                 summon_levels=SUMMON_LEVELS,
                 magic_levels=MAGIC_LEVELS,
                 verbose=False):
    """Open a booster pack and return the contents."""
    cryptid_count = np.zeros(summon_levels.shape)
    magic_count = np.zeros(magic_levels.shape)
    for key in booster.keys():
        # get the card
        card = booster[key]
        # find if it is cryptid or magic
        mag_or_crypt = list(card)[0]
        # match the case
        match mag_or_crypt:
            case "cryptid":
                if verbose:
                    print(f"Opening {card}")
                summon_level = card["cryptid"]["summon_level"]
                if isinstance(summon_level, list):
                    p = card["cryptid"]["probability"]
                    r = random()
                    idx = sum(r > p)
                    if verbose:
                        print(f"p={p}, r={r}, sum(r > p)={idx}")
                    cryptid_count[summon_level[idx]] = cryptid_count[summon_level[idx]] + 1
                else:
                    cryptid_count[summon_level] = cryptid_count[summon_level] + 1
            case "magic":
                if verbose:
                    print(f"Opening {card}")
                magic_level = card["magic"]["magic_level"]
                if isinstance(magic_level, list):
                    p = card["magic"]["probability"]
                    r = random()
                    idx = sum(r > p)
                    if verbose:
                        print(f"p={p}, r={r}, sum(r > p)={idx}")
                    magic_count[magic_level[idx]] = magic_count[magic_level[idx]] + 1
                else:
                    magic_count[magic_level] = magic_count[magic_level] + 1
            case _:
                raise ValueError(f"unrecognised card: {mag_or_crypt}")
    return cryptid_count, magic_count


def see_probabilities():
    def make_text_surface(x, y, msg, font):
        text = font.render(msg, True, "Red")
        textRect = text.get_rect()
        textRect.left = x
        textRect.top = y
        return text, textRect

    pygame.init()
    screen = pygame.display.set_mode((600, 400))
    FONT = os.path.join("assets", "fonts", "Cabin_Sketch", "CabinSketch-Regular.ttf")

    # first line
    font = pygame.font.Font(FONT, 32)
    running = True
    # main count
    cryptid_count = np.zeros(SUMMON_LEVELS.shape)
    magic_count = np.zeros(MAGIC_LEVELS.shape)
    pause = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    pause = not pause

        if not pause:
            try:
                # open a booster
                crypt, mag = open_booster(verbose=False)

                cryptid_count = cryptid_count + crypt
                magic_count = magic_count + mag
                screen.fill((56, 56, 64))

                x = 100
                y = 20
                msg = "Cryptid type cards"
                screen.blit(*make_text_surface(x, y, msg.upper(), font))
                for i in SUMMON_LEVELS:
                    y += 30
                    msg = f"summon level {i}: {int(cryptid_count[i])}, [{int(cryptid_count[i]) / cryptid_count.sum() * 100: 0.1f} %]"
                    screen.blit(*make_text_surface(x, y, msg, font))

                y += 60
                msg = "Magic type cards"
                screen.blit(*make_text_surface(x, y, msg.upper(), font))
                for i in MAGIC_LEVELS:
                    y += 30
                    msg = f"Magic level {i}: {int(magic_count[i])}, [{int(magic_count[i]) / magic_count.sum() * 100: 0.1f} %]"
                    screen.blit(*make_text_surface(x, y, msg, font))

            except BaseException:
                print(traceback.format_exc())
                running = False

        else:
            screen.fill((56, 56, 64))
            screen.blit(*make_text_surface(x, 200, "PAUSED (hit enter)", font))

        pygame.display.update()
    pygame.quit()
    sys.exit()


# each card can be summoned with the following conditions these can be gacha rolled
SUMMON_TYPES = ["normal", "sacrifice", "on_damage", "mulling"]
PROBABILITY_PER_SUMMON_TYPE = np.ones((len(SUMMON_TYPES),)) * 1 / len(SUMMON_TYPES)
# there is also 1 iteration of type per class
DAMAGE_TYPES = ["blood", "sweat", "tears", "normal"]
PROBABILITY_PER_DAMAGE_TYPE = np.ones((len(DAMAGE_TYPES),)) * 1 / len(DAMAGE_TYPES)
# attack modifier
MODIFIERS = ["critical_strike", "poison", "life_steal", "stun", "mull", "normal"]
PROBABILITY_PER_MODIFIER_TYPE = np.ones((len(MODIFIERS),)) * 1 / len(MODIFIERS)
# attribute variability that can be gacha rolled
SUMMON_LEVEL_ATT_UPPER = [200, 400, 600, 800]
SUMMON_LEVEL_ATT_LOWER = [100, 200, 400, 600]
SUMMON_LEVEL_HP_UPPER = [250, 450, 650, 850]
SUMMON_LEVEL_HP_LOWER = [150, 250, 450, 650]
TYPE_CONTIRBUTION_UPPER = [20, 30, 40, 50]
TYPE_CONTIRBUTION_LOWER = [10, 20, 30, 40]


# strengths/weaknesses
TYPE_CHART = {
    "blood": {"weaknesses": ["cosmic"], "strengths": ["sweat"]},
    "sweat": {"weaknesses": ["blood"], "strengths": ["tears"]},
    "tears": {"weaknesses": ["sweat"], "strengths": ["physical"]},
    "physical": {"weaknesses": ["tears"], "strengths": ["technological"]},
    "technological": {"weaknesses": ["physical"], "strengths": ["cosmic"]},
    "cosmic": {"weaknesses": ["technological"], "strengths": ["blood"]}
}


def mint_cryptid(CLASS, SUMMON_LEVEL):
    """Mint the data for a cryptid card."""
    card_data = {}
    card_data["card_type"] = "cryptid"
    card_data["summon_level"] = SUMMON_LEVEL
    card_data["name"] = fake.name()
    card_data["class"] = CLASS
    r = random()
    p = np.cumsum(PROBABILITY_PER_SUMMON_TYPE)
    idx = sum(p <= r) - 1
    card_data["summon_type"] = SUMMON_TYPES[idx]
    r = random()
    p = np.cumsum(PROBABILITY_PER_DAMAGE_TYPE)
    idx = sum(p <= r) - 1
    card_data["damage_type"] = DAMAGE_TYPES[idx]
    r = random()
    p = np.cumsum(PROBABILITY_PER_MODIFIER_TYPE)
    idx = sum(p <= r) - 1
    card_data["modifier"] = MODIFIERS[idx]
    card_data["hp"] = randint(SUMMON_LEVEL_HP_LOWER[SUMMON_LEVEL], SUMMON_LEVEL_HP_UPPER[SUMMON_LEVEL])
    card_data["attack"] = randint(SUMMON_LEVEL_ATT_LOWER[SUMMON_LEVEL], SUMMON_LEVEL_ATT_UPPER[SUMMON_LEVEL])
    card_data["type_contribution"] = randint(TYPE_CONTIRBUTION_LOWER[SUMMON_LEVEL], TYPE_CONTIRBUTION_UPPER[SUMMON_LEVEL])
    return card_data


def mint_magic(CLASS, MAGIC_LEVEL):
    """Mint the data for a magic card."""
    card_data = {}
    card_data["card_type"] = "magic"
    card_data["magic_level"] = MAGIC_LEVEL
    card_data["name"] = fake.name()
    card_data["class"] = CLASS
    R = randint(1, 3)

    card_data["influence"] = {}
    card_data["influence"]["summon_type"] = None
    card_data["influence"]["damage_type"] = None
    card_data["influence"]["modifier"] = None

    match R:
        case 1:
            r = random()
            p = np.cumsum(PROBABILITY_PER_SUMMON_TYPE)
            idx = sum(p <= r) - 1
            card_data["influence"]["summon_type"] = SUMMON_TYPES[idx]

        case 2:
            r = random()
            p = np.cumsum(PROBABILITY_PER_DAMAGE_TYPE)
            idx = sum(p <= r) - 1
            card_data["influence"]["damage_type"] = DAMAGE_TYPES[idx]

        case 3:
            r = random()
            p = np.cumsum(PROBABILITY_PER_MODIFIER_TYPE)
            idx = sum(p <= r) - 1
            card_data["influence"]["modifier"] = MODIFIERS[idx]

    return card_data


def main():
    """Make the card stats."""
    # iterate each class of cryptid
    card_data = {}
    card_id = 1
    for CLASS in CLASSES:
        # make the cryptid cards
        for level, N in enumerate(N_CARDS_PER_X_PER_CLASS["summon_level"]):
            n = 0
            while n < N:
                card_data[card_id] = mint_cryptid(CLASS, level)
                n += 1
                card_id += 1
        # make the magic card
        for level, N in enumerate(N_CARDS_PER_X_PER_CLASS["magic_level"]):
            n = 0
            while n < N:
                card_data[card_id] = mint_magic(CLASS, level)
                n += 1
                card_id += 1

    # Delete the file if it already exists
    if os.path.exists(NFT_FNAME):
        string = input(prompt=f"{NFT_FNAME} will be overwritten. Type 'OK' to proceed.")
        if string == "OK":
            os.remove(NFT_FNAME)
        else:
            raise Exception(f"User declined to overwrite NFTs. Input was: {string}.")

    # Open a file for writing
    with open(NFT_FNAME, "w") as f:
        # Write the dictionary to the file in JSON format
        json.dump(card_data, f)

    return card_data


if __name__ == "__main__":
    # see_probabilities()
    nfts = main()
    print(nfts)
