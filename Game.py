from window import *
import decks
from Player import *
import time

class Game:
    def __init__(self):
        self.player1 = Player("Player 1", decks.random_deck())
        self.player2 = Player("Player 2", decks.random_deck())
        self.player1.set_enemy(self.player2)
        self.player2.set_enemy(self.player1)

        self.turn = True
        self.player1.start_turn()
    def switch_turn(self):
        self.turn = not self.turn
        if not self.turn:
            self.player1.end_turn()
            self.player2.start_turn()
            self.player2.random_turn()
            time.sleep(0.5)
            self.switch_turn()
        else:
            self.player2.end_turn()
            self.player1.start_turn()
            print(self.player2.battlefield.soldiers)
            print(self.player1.battlefield.soldiers)
        