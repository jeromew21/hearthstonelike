from Game import *

class TestGame(Game):
    def __init__(self):
        super().__init__()
    def play(self):
        while True:
            self.player1.random_turn(stall=False)
            self.player1.end_turn()
            self.turns += 1
            if self.game_status() is not None:
                break
            self.player2.start_turn()
            self.player2.random_turn(stall=False)
            self.player2.end_turn()
            self.turns += 1
            if self.game_status() is not None:
                break
            self.player1.start_turn()
        return self.game_status()

if __name__ == "__main__":
    p1wins = 0
    p2wins = 0
    games_simulated = 10000
    for i in range(games_simulated):
        result = AIGame().play()[1]
        if result == 1:
            p1wins += 1
        elif result == -1:
            p2wins += 1
    print("First player wins:", p1wins)
    print("Second player wins:", p2wins)
    print("First player wins {0:.2f} percent".format(100*(p1wins/games_simulated)))