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
    def game_status(self):
        if self.player1.health <= 0:
            return "{} wins".format(self.player2.name)
        if self.player2.health <= 0:
            return "{} wins".format(self.player1.name)
        return None
    def switch_turn(self):
        if self.player1.health <= 0:
            return
        if self.player2.health <= 0:
            return

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
        