"""Tools to interact with the NFT data."""
import os
import json

from nfts.generate_nfts import TYPE_CHART

# NFT details
NFT_FNAME = os.path.join(os.getcwd(), "nfts", "nft_info.json")
# Open the file for reading
with open(NFT_FNAME, "r") as f:
    # Load the contents of the file into a dictionary
    NFTS = json.load(f)


class Card(object):
    """Card class."""

    def __init__(self,
                 card_id: int):
        """
        Initialize the card.

        The card information is stored in our nft_info.json.
        it assumes that NFTS has been loaded in the init preamble such that it
        is a global variable.

        This class should be usable in the game, and therefore should be able
        to derive all the influences of attack power/modifiers/spell types etc.
        which ultimately results in an attack value being applied.
        """
        self.card_id = card_id
        details = NFTS[str(card_id)]
        self.name = details["name"]
        self.type = details["card_type"]

        # status about being played
        self.active = False
        self.turn_played = None

        if self.type == "cryptid":
            self.starting_hp = details["hp"]
            self.current_hp = details["hp"]
            self.attack = details["attack"]
            self.summon_level = details["summon_level"]
            self.cryptid_class = details["class"]
            self.summon_type = details["summon_type"]
            self.damage_type = details["damage_type"]
            self.modifier = details["modifier"]

            # card statuses
            self.can_attack = False
            self.summonable = False
            self.stunned = False
            self.stunned_for = 0
            self.dead = False

            # card features
            self.strength_dmg_multiplier = 1.5
            self.weakness_dmg_multiplier = 0.5

        elif self.type == "magic":
            self.magic_level = details['magic_level']
            self.name = details['name']
            self.magic_class = details['class']
            self.inf_summon = details['influence']['summon_type']
            self.inf_damage = details['influence']['damage_type']
            self.inf_modifier = details['influence']['modifier']

            # card statuses
            self.active_for = None

        else:
            raise ValueError(f"Unrecognised card type: {self.type}")

    def __repr__(self):
        """Print information when print(self) is called."""
        if self.type == "cryptid":
            return f"""----------------------------------
Cryptid Card {self.card_id}: {self.name}.
----------------------------------
Class:        {self.cryptid_class}
Level:        {self.summon_level}
Health:       {self.current_hp} / {self.starting_hp}
Attack:       {self.attack}
Summon type:  {self.summon_type}
Damage type:  {self.damage_type}
Modifier:     {self.modifier}

Alive:      {'False' if self.dead else 'True'}
Stunned:    {'True' if self.stunned else 'False'}
Summonable: {'True' if self.summonable else 'False'}
----------------------------------
"""
        elif self.type == "magic":
            return f"""----------------------------------
Magic Card {self.card_id}: {self.name}.
----------------------------------
Class:        {self.magic_class}
Level:        {self.magic_level}
Influences:
    Summon:    {self.inf_summon}
    Damage:    {self.inf_damage}
    Modifier:  {self.inf_modifier}
----------------------------------
"""

    def receive_damage(self, damage: int) -> int:
        """Apply damage to the card. Type damage should be accounted for."""
        new_hp = max([0, self.current_hp - damage])
        excess_damage = abs(min([0, self.current_hp - damage]))
        self.current_hp = new_hp
        if self.current_hp <= 0:
            self.dead = True
        return excess_damage

    def attack_on_type(self, recipient_type: str) -> None:
        """Calculate damage to be applied to a different card."""
        # load the type chart
        strengths = TYPE_CHART[self.damage_type]["strengths"]
        weaknesses = TYPE_CHART[self.damage_type]["weaknesses"]
        # calculate the final damage
        if recipient_type in strengths:
            dmg = self.attack * self.strength_dmg_multiplier
        elif recipient_type in weaknesses:
            dmg = self.attack * self.weakness_dmg_multiplier
        if recipient_type in strengths and recipient_type in weaknesses:
            dmg = self.attack
        # return the damage applied
        return int(dmg)

    def summon(self):
        """Summon the card based on condition."""
        if True:
            self.summonable = True

    def play_card(self, turn_played):
        """Play the card."""
        self.active = True
        self.turn_plyed = turn_played
        # note that update_on_turn will be called after this.
        return self

    def be_stunned(self, stunned_for_n_turns):
        """Apply a stun on the card."""
        self.stunned = True
        self.stunned_for = stunned_for_n_turns

    def is_active(self) -> bool:
        """Check if card is active."""
        return self.active

    def is_dead(self) -> bool:
        """Check if cryptid is dead."""
        if self.type == "cryptid":
            return self.dead
        else:
            raise TypeError(f"Not a cryptid card, instead type {self.type}")

    def is_stunned(self) -> bool:
        """Check if cryptid is stunned."""
        if self.type == "cryptid":
            return self.stunned
        else:
            raise TypeError(f"Not a cryptid card, instead type {self.type}")

    def is_summonable(self) -> bool:
        """Check if cryptid is summonable."""
        if self.type == "cryptid":
            return self.summonable
        else:
            raise TypeError(f"Not a cryptid card, instead type {self.type}")

    def update_on_turn_end(self, current_turn):
        """Update card statuses at the end of current turn."""
        if self.is_active():
            match self.type:
                case "cryptid":
                    # reduce the stun timer if stunned
                    if self.stunned_for > 0:
                        self.stunned_for -= 1
                        self.stunned = True
                    else:
                        self.stunned = False
                        self.stunned_for = 0

                    # cannot attack when dead
                    if self.is_dead():
                        self.can_attack = False
                    # cannot attack when summoned
                    elif self.turn_played == current_turn:
                        self.can_attack = False
                    # cannot attack when stunned
                    elif self.is_stunned():
                        self.can_attack = False
                    else:
                        self.can_attack = True

                case "magic":
                    # if the magic card is active, reduce it's effect time
                    if self.active_for > 0:
                        self.active_for -= 1
                    else:
                        # if effect time has expired, set to not active.
                        self.active_for = None
                        self.active = False
