from DeckHand import Deck, Hand
from Battlefield import Battlefield
from Powers import *

import random, time

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
        self.base_power = Ship()
        self.say = lambda s: print(s)
        self.can_use_power = False
    def set_enemy(self, enemy):
        self.enemy = enemy
        self.battlefield.set_enemy(enemy)
    def start_turn(self): #ai would act here
        self._mana = (self._mana[0] + 1, self._mana[1] + 1)
        self._mana = (self._mana[1], self._mana[1])
        self.draw_card()
        self.battlefield.start_turn()
        self.spell = None
        self.spell_targets = None
        self.can_use_power = True
    def end_turn(self):
        self.battlefield.end_turn()
        self.can_use_power = False
    def use_power(self):
        if self.can_use_power:
            self.base_power.play(self, self.enemy)
            self.can_use_power = False
    @property
    def mana(self):
        return self._mana[0]
    @property
    def mana_str(self):
        return "{}/{}".format(*self._mana)
    def take_damage(self, damager, damage):
        self.health -= damage
    def spend_mana(self, m):
        self._mana = (self._mana[0] - m, self._mana[1])
    def soldier_attack(self, index, enemy):
        if self.battlefield.can_attack(index, enemy):
            self.battlefield.soldiers[index].do_attack(enemy)
            self.clean_up()
            return True
        return False
    def draw_card(self):
        card = self.deck.draw()
        if card is not None:
            self.hand.add_card(card)
    def clean_up(self):
        self.battlefield.soldiers = [
            s for s in self.battlefield.soldiers if s.health > 0
        ]
        self.enemy.battlefield.soldiers = [
            s for s in self.enemy.battlefield.soldiers if s.health > 0
        ]
    def play_card(self, index):
        if self.hand.can_play(index, self, self.enemy):
            card = self.hand.throw(index).play(self, self.enemy)
            self.say("{} played {}".format(self.name, card))
            self.clean_up()
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
        self.say("Waiting to cast {}".format(spell))
        self.spell = spell
        self.spell_targets = self.constrain_targets(constraint)
        if not self.spell_targets:
            self.spell = None
    def cast(self, target):
        if target in self.spell_targets:
            self.say("Casting {} on {}".format(self.spell, target))
            self.spell.cast(target)
            self.spell = None
            self.spell_targets = None
            self.clean_up()
    def input_target(self, constraint="any"):
        targets = self.constrain_targets(constraint)
        if not targets:
            return False
        n = 0
        for k in targets:
            self.say(n, str(k))
            n += 1
        while True:
            try:
                i = int(input("Target:"))
                if i < 0 or i >= len(targets):
                    raise ZeroDivisionError("oops")
                break
            except (ZeroDivisionError, ValueError):
                self.say("Invalid input.")
        return targets[i]
    def random_turn(self, stall=True):
        li = list(range(self.hand.size))
        random.shuffle(li)
        for i in li:
            if self.play_card(i) and stall:
                time.sleep(random.random() * 2)
            if self.spell:
                if self.spell_targets:
                    if stall:
                        time.sleep(random.random() * 2)
                    self.cast(random.choice(self.spell_targets))
                else:
                    break
        sols = list(range(self.battlefield.size))
        random.shuffle(sols)
        for s in sols:
            for e in [self.enemy] + self.enemy.battlefield.soldiers:
                if self.soldier_attack(s, e) and stall:
                    time.sleep(random.random() * 2)
        

class AIPlayer(Player):
    pass
