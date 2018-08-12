from cards import *
from DeckHand import *

def bois():
    return Deck([Boi() for i in range(15)] + \
        [DirectDamageSpell() for i in range(15)])

