"""Tools to interact with the NFT data."""
import os
import json

# NFT details
NFT_FNAME = os.path.join(os.getcwd(), "nfts", "nft_info.json")
# Open the file for reading
with open(NFT_FNAME, "r") as f:
    # Load the contents of the file into a dictionary
    NFTS = json.load(f)


class Card(object):
    """Card class."""

    def __init__(self,
                 card_id: int,
                 name: str = "John"):  # !!! update card inputs
        """Initialize the card."""
        self.card_id = card_id
        details = NFTS[str(card_id)]
        self.name = details["name"]
        self.type = details["card_type"]

        if self.type == "cryptid":
            self.starting_hp = details["hp"]
            self.current_hp = details["hp"]
            self.attack = details["attack"]
            self.summon_level = details["summon_type"]
            self.dead = False

        elif self.type == "magic":
            pass

    def __repr__(self):
        """Print information when print(self) is called."""
        return f"""Card {self.card_id}: {self.name}.
    Health: {self.current_hp} / {self.starting_hp}
    Attack: {self.attack}
    Status: {'Dead' if self.dead else 'Alive'}
"""

    def receive_damage(self, damage: int) -> int:
        """Apply damage to the card."""
        excess_damage = max([0, self.current_hp - damage])
        self.current_hp -= damage - excess_damage
        if self.current_hp <= 0:
            self.dead = True
        return excess_damage
