class Card:
    cost = 1
    name = "Card"
    can_attack = False
    def can_play(self, player, enemy):
        return player.mana >= self.cost
    def play(self, player, enemy):
        player.spend_mana(self.cost)
        return self
    @property
    def display_name(self):
        return self.name
    @property
    def display_subtext(self):
        return "{}\n{}❂".format(self.subtext, self.cost)
    @property
    def subtext(self):
        return "card"
    def __str__(self):
        return self.name

class Soldier(Card):
    health = 2
    attack = 2
    cost = 2
    name = "Soldier"
    info = "A soldier"
    def __init__(self):
        self._can_attack = False
    def can_play(self, player, enemy):
        if player.mana >= self.cost:
            if not player.battlefield.full:
                return True
        return False
    @property
    def subtext(self):
        return "{}/{}".format(self.attack, self.health)
    def play(self, player, enemy):
        super().play(player, enemy)
        player.battlefield.add_soldier(self)
        self.battlecry(player, enemy)
        self._can_attack = False
        return self
    def battlecry(self, player, enemy):
        pass
    @property
    def can_attack(self):
        return self._can_attack
    def start_turn(self):
        self._can_attack = True
    def end_turn(self):
        self._can_attack = False
    def take_damage(self, damage):
        self.health -= damage
    def do_attack(self, target):
        target.take_damage(self.attack)
        self.take_damage(target.attack)
        self._can_attack = False

class Spell(Card):
    pass