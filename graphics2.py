import sys
import pygame

def color(c):
    colors = {
        "red": (255, 0, 0),
        "green": (0, 255, 0),
        "blue": (0, 0, 255),
        "darkBlue": (0, 0, 128),
        "white": (255 , 255, 255),
        "black": (0, 0, 0),
        "pink": (255, 200, 200),
        "gray": (180, 180, 180),
        "magenta": (255, 0, 255),
        "lime": (0, 255, 0),
        "yellow": (255, 255, 0),
        "purple": (161, 33,	240),
        "orange": (255, 0, 166)
    }
    return colors.get(c, (255,255,255))

class Point:
    def __init__(self, x, y):
        self._x = x
        self._y = y
    def getX(self):
        return self._x
    def getY(self):
        return self._y
    def real_x(self, win):
        return self._x
    def real_y(self, win):
        return win.height - self._y
    def __repr__(self):
        return "Point({}, {})".format(self._x, self._y)

class Drawable:
    def __init__(self):
        self.thickness = 1
        self.color = color("white")
        self.outline = color("black")
        self._win = None
    def draw(self, win):
        win._add_object(self)
        self._win = win
    def undraw(self):
        if self._win is not None:
            self._win._rem_object(self)
    def setOutline(self, c):
        self.outline = color(c)
    def setWidth(self, i):
        self.thickness = int(i)

class Line(Drawable):
    def __init__(self, p1, p2):
        super().__init__()
        self.p1 = p1
        self.p2 = p2
    def update(self, win):
        pygame.draw.lines(win.screen, 
            self.outline, False, 
            [
                (self.p1.real_x(win), self.p1.real_y(win)), 
                (self.p2.real_x(win), self.p2.real_y(win))
            ], self.thickness)

class Text(Drawable):
    def __init__(self, p, label):
        super().__init__()
        self.label = label
        self.p = p
        self.font = pygame.font.Font("seguisym.ttf", 15)
    def setSize(self, s):
        self.font = pygame.font.Font("seguisym.ttf", s + 5)
    def setText(self, t):
        self.label = t
    def update(self, win):
        y_offset = 0
        net_offset = None
        lines = self.label.split("\n")
        for line in lines:
            label = self.font.render(line, True, self.outline)
            w = label.get_width()
            h = label.get_height()
            if not net_offset:
                net_offset = (len(lines)-1) * h * 0.5
            win.screen.blit(label, (
                self.p.real_x(win) - w/2,
                self.p.real_y(win) - h/2 + y_offset - net_offset,
            ))
            y_offset += h

class Rectangle(Drawable):
    def __init__(self, p1, p2):
        super().__init__()
        self.p1 = p1
        self.p2 = p2
    def setFill(self, c):
        self.color = color(c)
    def getCenter(self):
        w = (self.p2.getX() - self.p1.getX()) / 2
        h = (self.p2.getY() - self.p1.getY()) / 2
        return Point(
            self.p1.getX() + w,
            self.p1.getY() + h
        )
    def update(self, win):
        x = self.p1.real_x(win)
        y = self.p2.real_y(win)
        width = self.p2.real_x(win) - self.p1.real_x(win)
        height = self.p1.real_y(win) - self.p2.real_y(win)
        # fill
        if self.color != color("white"):
            pygame.draw.rect(win.screen, self.color, 
                (x, y, width, height), 
                0) 
        # outline
        pygame.draw.rect(win.screen, self.outline, 
            (x, y, width, height), 
            self.thickness)
    def getP1(self):
        return self.p1
    def getP2(self):
        return self.p2

class GraphWin:
    def __init__(self, title, width, height, icon=None):
        self.width = width
        self.height = height
        self.title = title
        self._objects = []

        pygame.init()
        self.font = pygame.font.Font("seguisym.ttf", 15)

        pygame.display.set_caption(self.title)
        if icon:
            sur = pygame.image.load(icon)
            pygame.display.set_icon(sur)
        self.screen = pygame.display.set_mode(
            (self.width, self.height))
        self.screen.fill(color("white"))
        pygame.display.update()
    def getMouse(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    point = Point(
                        pos[0],
                        self.height - pos[1]
                    )
                    return point
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            self.screen.fill(color("white"))
            for obj in self._objects:
                obj.update(self)
            pygame.display.update()
    def _add_object(self, o):
        if o in self._objects:
            raise Exception("Object already drawn")
        self._objects.append(o) 
    def _rem_object(self, o):
        if o in self._objects:
            self._objects.remove(o)
    def setCoords(self, *args):
        pass
        
if __name__ == "__main__":
    g = GraphWin("Test", 640, 480)
    r = Rectangle(Point(100, 100), Point(150, 150))
    r.draw(g)
    while True:
        g.getMouse()
        r.setFill("red")