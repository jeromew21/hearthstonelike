import random

class Deck:
    max_size = 30

    def __init__(self, cards):
        self.cards = cards
        self.initial_size = len(cards)
    def shuffle(self):
        random.shuffle(self.cards)
    @property
    def size(self):
        return len(self.cards)
    def draw(self):
        if self.size == 0:
            return None
        return self.cards.pop()
    def place_on_top(self, card):
        self.cards.append(card)
    def insert(self, card):
        self.cards.insert(card, random.randint(0, len(self.cards) - 1))

class Hand:
    max_size = 7
    starting_size = 4

    def __init__(self, deck):
        self.cards = [deck.draw() for i in range(self.starting_size)]
    def add_card(self, card):
        if self.size < self.max_size:
            self.cards.append(card)
    @property
    def size(self):
        return len(self.cards)
    def clear(self):
        self.cards = []
    def show(self):
        print("Hand:")
        for card in self.cards:
            print(card)
    def throw(self, i):
        return self.cards.pop(i)
    def can_play(self, i, player, enemy):
        return i >= 0 and i < self.size and self.cards[i].can_play(player, enemy)
        