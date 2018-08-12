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

class Raptor(Soldier):
    attack = 3
    health = 2
    cost = 2
    name = "Raptor"
    info = "Kawhi Leonard"

class Yeti(Soldier):
    attack = 4
    health = 5
    cost = 4
    name = "Abominable Snowman"
    display_name = "Abominable\nSnowman"
    info = "Who ya gonna call"

class Nuke(DirectDamageSpell):
    damage = 10
    cost = 10
    name = "Nuke"