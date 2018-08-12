from Card import Soldier, Spell

class DirectDamageSpell(Spell):
    damage = 1
    cost = 1
    name = "Direct Damage"
    constraint = "any"
    @property
    def subtext(self):
        return "{} damage".format(self.damage)
    @property
    def info(self):
        return "Do {} damage".format(self.damage)
    def play(self, player, enemy):
        player.set_spell(self, "any")
        return super().play(player, enemy)
    def cast(self, target):
        target.take_damage(self.damage)


class Boi(Soldier):
    attack = 1
    health = 1
    cost = 1
    name = "Boi"
    info = "A little boi"

class Nuke(DirectDamageSpell):
    damage = 10
    cost = 10
    name = "Nuke"