from graphics import *
import sys

WIDTH = 1280
HEIGHT = 900

class Clickable:
    registry = []
    def __init__(self, label, p1, p2, w, onclick=lambda:None, args=(), is_card=True):
        self._rect = Rectangle(p1, p2)
        self._rect.setFill("gray")
        self._label = label
        self._text = Text(self._rect.getCenter(), self._label)
        self._text.setSize(15)
        self._onclick = onclick
        self._args = args
        self._toggle = False
        self._icolor = "gray"
        self._scolor = "green"
        self._is_filled = False
        self._text2 = Text(Point(
            self._rect.getCenter().getX(), 
            self._rect.getCenter().getY() - 50), "")
        self.w = w
        self.card = None
        self.is_card = is_card
        Clickable.registry.append(self)
    def set_main_text(self, t):
        self._text.setText(t)
    def set_card(self, card):
        if not self.card is card:
            self.card = card
            self._toggle = False
        self._text.setText(card.display_name)
        if self.is_card:
            self._text2.setText(card.display_subtext)
        else:
            self._text2.setText(card.subtext)
        self._text2.undraw()
        self._text2.draw(self.w)
        self._icolor = "yellow" if card.can_attack else "white"
        self._scolor = "lime" if card.can_attack else "purple"
        if self._toggle:
            self._rect.setFill(self._scolor)
        else:
            self._rect.setFill(self._icolor)
    def remove_card(self):
        self.card = None
        self._icolor = "gray"
        self._scolor = "green"
        self._text.setText("Empty")
        self._text2.undraw()
        if self._toggle:
            self._rect.setFill(self._scolor)
        else:
            self._rect.setFill(self._icolor)
    def toggle_off(self):
        self._toggle = False
        self._rect.setFill(self._icolor)
    def toggle(self):
        self._toggle = not self._toggle
        if self._toggle:
            self._rect.setFill(self._scolor)
        else:
            self._rect.setFill(self._icolor)
    @classmethod
    def register(self, p):
        for cl in self.registry:
            if cl.in_bounds(p):
                cl.trigger()
    def in_bounds(self, p):
        ll, ur = self._rect.getP1(), self._rect.getP2()
        x, y = p.getX(), p.getY()
        return x > ll.getX() and x < ur.getX() \
            and y > ll.getY() and y < ur.getY()
    def trigger(self):
        self._onclick(*self._args)
    def draw(self, foo=None):
        self._rect.draw(self.w)
        self._text.draw(self.w)
    def set_onclick(self, c):
        self._onclick = c

class KOCWindow:
    def __init__(self, game):
        self.game = game
        self.win = GraphWin("KOC", width=WIDTH, height=HEIGHT) # create a window
        self.win.setCoords(0, 0, WIDTH, HEIGHT) # set the coordinates of the window; bottom left is (0, 0) and top right is (10, 10)
        
        dividing_line = HEIGHT * 0.63

        Line(Point(0, dividing_line), 
            Point(WIDTH, dividing_line)).draw(self.win)
        self.end_turn_button = Clickable(
            "End Turn", 
            Point(0, HEIGHT-100),
            Point(100, HEIGHT),  self.win, lambda: self.handle_end_turn()
        )
        self.end_turn_button.draw()

        self.battlefield1 = []
        self.battlefield2 = []
        self.hand1 = []

        count = 5
        size = WIDTH//10
        offset = (WIDTH/2) - (size*(count/2))
        padding = size//6
        for g in (False, True): #broke bc backwards rects
            for i in range(count):
                if not g:
                    p1 = Point(offset + i*size, dividing_line+padding)
                    p2 = Point(offset+size + (i*size), dividing_line+size+padding)
                else:
                    p1 = Point(offset + i*size, dividing_line-size-padding)
                    p2 = Point(offset+size + (i*size), dividing_line-padding)

                soldierCell = Clickable(
                    "Empty",
                    p1, p2, self.win,
                    lambda isP1, index: self.handle_soldier_click(isP1, index),
                    args=(g,i), is_card=False
                )
                soldierCell.draw()

                if g:
                    self.battlefield1.append(soldierCell)
                else:
                    self.battlefield2.append(soldierCell)

        count = 7
        wth = WIDTH//8
        hgt = HEIGHT//4
        offset = (WIDTH/2) - (wth*(count/2))
        padding = size + padding*2
        for i in range(count):
            p1 = Point(offset + i*wth, dividing_line-hgt-padding)
            p2 = Point(offset+wth + (i*wth), dividing_line-padding)

            handCell = Clickable(
                "Empty",
                p1, p2, self.win,
                lambda k: self.handle_hand_click(k),
                args=(i,)
            )
            handCell.draw()
            self.hand1.append(handCell)

        self.turn_text = Text(Point(90, HEIGHT - 150), "Your turn")
        self.deck_text = Text(Point(90, 40), "{} cards in deck".format(""))
        self.mana_text = Text(Point(90, 20), "{}/{} mana".format("", ""))
        self.enemy_deck_text = Text(
            Point(WIDTH - 90, HEIGHT - 40), "{} cards in deck".format(""))
        self.enemy_mana_text = Text(
            Point(WIDTH - 90, HEIGHT - 20), "{}/{} mana".format("", ""))
        self.enemy_hand_text = Text(
            Point(WIDTH - 90, HEIGHT - 60), "{} cards in hand".format(""))
        self.turn_text.setSize(15)
        self.deck_text.setSize(15)
        self.mana_text.setSize(15)
        self.enemy_deck_text.setSize(15)
        self.enemy_mana_text.setSize(15)
        self.enemy_hand_text.setSize(15)
        self.turn_text.draw(self.win)
        self.deck_text.draw(self.win)
        self.mana_text.draw(self.win)
        self.enemy_deck_text.draw(self.win)
        self.enemy_mana_text.draw(self.win)
        self.enemy_hand_text.draw(self.win)

        base_size = size
        self.enemy_target = Clickable("30", 
            Point(WIDTH/2 - base_size/2, HEIGHT - base_size), 
            Point(WIDTH/2 + base_size/2, HEIGHT), self.win,
            self.handle_enemy_click, ()
        )
        self.player_target = Clickable("30", 
            Point(WIDTH/2 - base_size/2, 0), 
            Point(WIDTH/2 + base_size/2, base_size), self.win,
            self.handle_base_click, ()
        )
        self.enemy_target.draw()
        self.player_target.draw()

        self._active_card_index = None

        self._active_soldier_index = None
        self._active_soldier_outline = Rectangle(Point(0, 0), Point(0, 0))
        self._allowed_targets = []

        self.update_all()

    def update_all(self):
        self.turn_text.setText("Your turn" if self.game.turn else "Enemy turn")
        self.deck_text.setText("{} cards in deck".format(self.game.player1.deck.size))
        self.mana_text.setText("{} mana".format(self.game.player1.mana_str))
        self.enemy_deck_text.setText("{} cards in deck".format(self.game.player2.deck.size))
        self.enemy_mana_text.setText("{} mana".format(self.game.player2.mana_str))
        self.enemy_hand_text.setText("{} cards in hand".format(self.game.player2.hand.size))
        
        self.enemy_target.set_main_text(str(self.game.player2.health))
        self.player_target.set_main_text(str(self.game.player1.health))

        k = -1
        for i, card in enumerate(self.game.player1.hand.cards):
            self.hand1[i].set_card(card)
            k = i
        k += 1
        if k < 7:
            for i in range(k, len(self.hand1)):
                self.hand1[k].remove_card()
        
        for g in (True, False):
            if g:
                soldiers = self.game.player1.battlefield.soldiers
                bf = self.battlefield1
            else:
                soldiers = self.game.player2.battlefield.soldiers
                bf = self.battlefield2

            k = -1
            for i, card in enumerate(soldiers):
                bf[i].set_card(card)
                k = i
            k += 1
            if k < 7:
                for i in range(k, len(bf)):
                    bf[k].remove_card()

    def set_activeSI(self, i):
        self._active_soldier_index = i
        r = self.battlefield1[i]._rect
        self._active_soldier_outline.undraw()
        self._active_soldier_outline = Rectangle(
            r.getP1(),
            r.getP2()
        )
        self._active_soldier_outline.setWidth("6")
        self._active_soldier_outline.setOutline("orange")
        self._active_soldier_outline.draw(self.win)

        for k in self._allowed_targets:
            k.undraw()
        self._allowed_targets = []
        for en in self.battlefield2 + [self.enemy_target]:
            if (en.card and \
                self.game.player1.battlefield.can_attack(
                    i, en.card)) or (en is self.enemy_target and \
                self.game.player1.battlefield.can_attack(
                    i, self.game.player2)):
                rect = Rectangle(
                    en._rect.getP1(),
                    en._rect.getP2()
                )
                rect.setWidth("6")
                rect.setOutline("magenta")
                rect.draw(self.win)
                self._allowed_targets.append(rect)
    def unset_activeSI(self):
        self._active_soldier_outline.undraw()
        for i in self._allowed_targets:
            i.undraw()
        self._allowed_targets = []
        self._active_soldier_index = None
    def set_targets(self, targets):
        self._allowed_targets = []
        for t in self.battlefield1 + self.battlefield2 + \
            [self.player_target, self.enemy_target]:
            if (t.card and t.card in targets) or \
                (t is self.player_target and \
                self.game.player1 in targets) or \
                (t is self.enemy_target and \
                self.game.player2 in targets):
                rect = Rectangle(
                    t._rect.getP1(),
                    t._rect.getP2()
                )
                rect.setWidth("6")
                rect.setOutline("magenta")
                rect.draw(self.win)
                self._allowed_targets.append(rect)
    def clear_targets(self):
        for i in self._allowed_targets:
            i.undraw()
        self._allowed_targets = []
    def handle_end_turn(self):
        if self.game.player1.spell:
            return
        self.game.switch_turn()
        self.update_all()
        self.unset_activeSI()
    def handle_hand_click(self, index):
        button = self.hand1[index]
        for i in self.hand1:
            if i is not button:
                i.toggle_off()
        button.toggle()

        if self.game.player1.spell:
            return

        if self._active_card_index is None:
            self._active_card_index = index
            self.unset_activeSI()
        elif self._active_card_index == index:
            self._active_card_index = None
            if not self.game.player1.play_card(index):
                print("Can't play that card")
            else:
                if self.game.player1.spell:
                    self.set_targets(self.game.player1.spell_targets)
                self.update_all()
    def handle_soldier_click(self, isP1, index):
        if isP1:
            button = self.battlefield1[index]
        else:
            button = self.battlefield2[index]
        for i in self.battlefield1 + self.battlefield2:
            if not i is button:
                i.toggle_off()

        if self.game.player1.spell:
            if button.card and button.card in self.game.player1.spell_targets:
                self.game.player1.cast(button.card)
                self.clear_targets()
                self.update_all()
            return

        button.toggle()
        if self._active_soldier_index is None:
            if isP1 and button.card and button.card.can_attack:
                self.set_activeSI(index)
            else:
                self.unset_activeSI()
        else:
            if not self.game.player1.soldier_attack(self._active_soldier_index, button.card):
                print("Can't attack there")
                self.unset_activeSI()
            else:
                self.update_all()
                self.unset_activeSI()
    def handle_base_click(self):
        if self.game.player1.spell:
            if self.game.player2 in self.game.player1.spell_targets:
                self.game.player1.cast(self.game.player1)
                self.clear_targets()
                self.update_all()
            return
    def handle_enemy_click(self):
        if self.game.player1.spell:
            if self.game.player2 in self.game.player1.spell_targets:
                self.game.player1.cast(self.game.player2)
                self.clear_targets()
                self.update_all()
            return

        if self._active_soldier_index is not None:
            if not self.game.player1.soldier_attack(self._active_soldier_index, self.game.player2):
                print("Can't attack base")
            else:
                print("FACE IS PLACE")
                self.update_all()
                self.unset_activeSI()
    def loop(self):
        while True:
            mouse = self.win.getMouse()
            Clickable.register(mouse)       
