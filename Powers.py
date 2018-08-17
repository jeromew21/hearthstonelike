from Card import BasePower
from cards import Boi, DirectDamageSpell

class Castle:
    name = "Castle"
    info = "Summon a 1/1"
    def play(self, player, enemy):
        if not player.battlefield.full:
            player.battlefield.add_soldier(Boi())

class Ship:
    name = "Ship"
    info = "Do 1 damage"
    def play(self, player, enemy):
        DirectDamageSpell().play(player, enemy)