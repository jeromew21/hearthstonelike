from Card import Soldier, Spell

class DirectDamageSpell(Spell):
    damage = 1
    name = "Direct Damage"
    @property
    def info(self):
        return "Do {} damage".format(self.damage)
    def play(self, player, enemy):
        super().play(player, enemy)
        player.get_target().take_damage(self.damage)

class Boi(Soldier):
    attack = 1
    health = 1
    cost = 1
    name = "Boi"
    info = "A little boi"
