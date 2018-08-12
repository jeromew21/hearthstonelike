from DeckHand import Deck, Hand
from Battlefield import Battlefield

from multiprocessing.pool import ThreadPool

class Player:
    attack = 0
    def __init__(self, name, deck):
        self.name = name
        self.deck = deck
        self.deck.shuffle()
        self.hand = Hand(self.deck)
        self.health = 30
        self.battlefield = Battlefield(self)
        self._mana = (0, 0)
        self.spell = None
        self.spell_targets = None
        self.graveyard = []
    def set_enemy(self, enemy):
        self.enemy = enemy
        self.battlefield.set_enemy(enemy)
    def start_turn(self): #ai would act here
        self._mana = (self._mana[0] + 1, self._mana[1] + 1)
        self._mana = (self._mana[1], self._mana[1])
        self.draw_card()
        self.battlefield.start_turn()
    def end_turn(self):
        self.battlefield.end_turn()
    @property
    def mana(self):
        return self._mana[0]
    @property
    def mana_str(self):
        return "{}/{}".format(*self._mana)
    def take_damage(self, damage):
        self.health -= damage
    def spend_mana(self, m):
        self._mana = (self._mana[0] - m, self._mana[1])
    def soldier_attack(self, index, enemy):
        if self.battlefield.can_attack(index, enemy):
            self.battlefield.soldiers[index].do_attack(enemy)
            return True
        return False
    def draw_card(self):
        card = self.deck.draw()
        self.hand.add_card(card)
    def clean_up(self):
        self.battlefield.soldiers = [
            s for s in self.battlefield.soldiers if s.health > 0
        ]
    def play_card(self, index):
        if self.hand.can_play(index, self, self.enemy):
            card = self.hand.throw(index).play(self, self.enemy)
            print("{} played {}".format(self.name, card))
            self.clean_up()
            self.enemy.clean_up()
            return True
        return False
    def __str__(self):
        return self.name
    def constrain_targets(self, constraint):
        if constraint == "any":
            targets = self.battlefield.soldiers + \
                self.enemy.battlefield.soldiers + \
                [self, self.enemy]
        elif constraint == "enemies":
            targets = self.enemy.battlefield.soldiers + \
                [self.enemy]
        elif constraint == "soldiers":
            targets = self.enemy.battlefield.soldiers + \
                self.battlefield.soldiers
        elif constraint == "enemy soldiers":
            targets = self.enemy.battlefield.soldiers
        elif constraint == "friendlies":
            targets = self.battlefield.soldiers + [self]
        elif constraint == "bases":
            targets = [self, self.enemy]
        else:
            targets = []
        return targets
    def set_spell(self, spell, constraint="any"):
        self.spell = spell
        self.spell_targets = self.constrain_targets(constraint)
        if not self.spell_targets:
            self.spell = None
    def cast(self, target):
        if target in self.spell_targets:
            self.spell.cast(target)
            self.spell = None
            self.spell_targets = None
            self.clean_up()
            self.enemy.clean_up()
    def input_target(self, constraint="any"):
        targets = self.constrain_targets(constraint)
        if not targets:
            return False
        n = 0
        for k in targets:
            print(n, str(k))
            n += 1
        while True:
            try:
                i = int(input("Target:"))
                if i < 0 or i >= len(targets):
                    raise ZeroDivisionError("oops")
                break
            except (ZeroDivisionError, ValueError):
                print("Invalid input.")
        return targets[i]
    
class AIPlayer(Player):
    pass
