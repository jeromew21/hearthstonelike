from Game import Game
from window import KOCWindow

if __name__ == "__main__":
    g = Game()
    k = KOCWindow(g)
    k.loop()