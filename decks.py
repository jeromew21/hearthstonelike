from DeckHand import *
from cards import *
import random

ALL_CARDS = [
    Boi, Nuke, Yeti, Firebreath, Raptor, Sharpsword,
    Mulligan, Archer, Cobra, FastForward, 
    ReachOut, AssasinationPlot, PlotArmor, Shrink,
    Duo, GeneticFreak, Kamikaze, LoneWolf
]

def bois():
    return Deck([Boi() for i in range(15)] + \
        [DirectDamageSpell() for i in range(15)])

def random_deck():
    return Deck([random.choice(ALL_CARDS)() for i in range(30)])
