from DeckHand import Deck, Hand
from Battlefield import Battlefield

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
    def play_card(self, index):
        if self.hand.can_play(index, self, self.enemy):
            card = self.hand.throw(index).play(self, self.enemy)
            print("{} played {}".format(self.name, card))
            return True
        return False
    def get_target(self):
        print("Targets:")
        targets = self.battlefield + self.enemy.battlefield + \
            [self, self.enemy]
        n = 0
        for k in targets:
            print(n, str(k))
            n += 1
        while True:
            try:
                i = int(input("Target:"))
                if i < 0 or i >= len(targets):
                    raise Exception("oops")
            except:
                print("Invalid input.")
        return targets[i]

class GUIPlayer(Player):
    def _get_target(self):
        while True:
            break
        return 0
    

