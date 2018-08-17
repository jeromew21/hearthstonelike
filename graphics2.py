import sys
import threading
import time
import pygame
from copy import deepcopy as _deepcopy


frames_per_second = 30


_colors = {
    "red": (255, 0, 0),
    "green": (0, 255, 0),
    "blue": (0, 0, 255),
    "white": (255 , 255, 255),
    "black": (0, 0, 0),
    "pink": (255, 200, 200),
    "gray": (180, 180, 180),
    "magenta": (255, 0, 255),
    "lime": (0, 255, 0),
    "yellow": (255, 255, 0),
    "purple": (161, 33, 240),
    "orange": (255, 0, 166)
}

def _color(c):
    return _colors.get(c, (255,255,255))


def color_rgb(r, g, b):
    return (r, g, b)


class Point:
    def __init__(self, x, y):
        self._x = x
        self._y = y
    def getX(self):
        return self._x
    def getY(self):
        return self._y
    def _real_x(self, win):
        if not win.coord_system:
            return self._x
        return self._x + win.xll
    def _real_y(self, win):
        if not win.coord_system:
            return self._y
        return win.yur - self._y
    def __repr__(self):
        return "Point({}, {})".format(self._x, self._y)
    def clone(self):
        return Point(self._x, self._y)


class _Pixel:
    def __init__(self, x, y, color, raw=False):
        self.raw = raw
        self.p = Point(x, y)
        self.color = _color(color)

    def draw(self, win):
        win._add_object(self)

    def _update(self, win):
        if not self.raw:
            coords = (self.p._real_x(win), self.p._real_y(win))
        else:
            coords = (self.p._x, self.p._y)
        win.screen.set_at(coords, self.color)


class Drawable:
    def __init__(self):
        self.thickness = 1
        self.color = _color("white")
        self.outline = _color("black")
        self._win = None

    def draw(self, win):
        win._add_object(self)
        self._win = win
        return self
    
    def move(self, dx, dy):
        pass

    def undraw(self):
        if self._win is not None:
            self._win._rem_object(self)

    def setOutline(self, c):
        self.outline = _color(c)

    def setWidth(self, i):
        self.thickness = int(i)

    def clone(self):
        return _deepcopy(self)


class Line(Drawable):
    def __init__(self, p1, p2):
        super().__init__()
        self.p1 = p1
        self.p2 = p2

    def getCenter(self):
        return Point((self.p1.getX()+self.p2.getX()) / 2,
            (self.p1.getY()+self.p2.getY()) / 2)
        
    def move(self, dx, dy):
        self.p1._x += dx
        self.p1._y += dy
        self.p2._x += dx
        self.p2._y += dy

    def _update(self, win):
        pygame.draw.lines(win.screen, 
            self.outline, False, 
            [
                (self.p1._real_x(win), self.p1._real_y(win)), 
                (self.p2._real_x(win), self.p2._real_y(win))
            ], self.thickness)


class Text(Drawable):
    def __init__(self, p, label):
        super().__init__()
        self.label = label
        self.p = p
        self.font_size = 15
        self.font_color = self.outline
        self.font_name = "seguisym.ttf"
        self._update_font()

    def _update_font(self):
        if self.font_name.endswith(".ttf"):
            self.font = pygame.font.Font(self.font_name, self.font_size)
        else:
            self.font = pygame.font.SysFont(self.font_name, self.font_size)

    def setFace(self, ff):
        self.font_name = ff
        self._update_font()
    
    def setSize(self, s):
        self.font_size = s + 5
        self._update_font()

    def setFill(self, c):
        self._color = _color(c)

    def setTextColor(self, c):
        self._color = _color(c)

    def setText(self, t):
        self.label = t
    
    def setStyle(self):
        pass

    def move(self, dx, dy):
        self.p._x += dx
        self.p._y += dy

    def draw(self, win):
        super().draw(win)
        return self
    
    def getAnchor(self):
        return self.p.clone()

    def _update(self, win):
        if self.font is None:
            return
        y_offset = 0
        net_offset = None
        lines = self.label.split("\n")
        for line in lines:
            label = self.font.render(line, True, self.font_color)
            w = label.get_width()
            h = label.get_height()
            if not net_offset:
                net_offset = (len(lines)-1) * h * 0.5
            win.screen.blit(label, (
                self.p._real_x(win) - w/2,
                self.p._real_y(win) - h/2 + y_offset - net_offset,
            ))
            y_offset += h


class Polygon(Drawable):
    def __init__(self, *points):
        super().__init__()
        self.points = points
    
    def getPoints(self):
        return [p.clone() for p in self.points]
    
    def move(self, dx, dy):
        for p in self.points:
            p._x += dx
            p._y += dy

    def _update(self, win):
        if self.color != win.bgcolor:
            pygame.draw.polygon(win.screen, self.color, 
                [[p._real_x(win), p._real_y(win)] for p in self.points], 0)
        pygame.draw.polygon(win.screen, self.outline, 
            [[p._real_x(win), p._real_y(win)] for p in self.points], self.thickness)


class Rectangle(Drawable):
    def __init__(self, p1, p2):
        super().__init__()
        self.p1 = p1
        self.p2 = p2
        self.isFilled = False

    def move(self, dx, dy):
        self.p1._x += dx
        self.p1._y += dy
        self.p2._x += dx
        self.p2._y += dy

    def setFill(self, c):
        self.isFilled = True
        self.color = _color(c)

    def getCenter(self):
        w = (self.p2.getX() - self.p1.getX()) / 2
        h = (self.p2.getY() - self.p1.getY()) / 2
        return Point(
            self.p1.getX() + w,
            self.p1.getY() + h
        )

    def _update(self, win):
        x = self.p1._real_x(win)
        y = self.p2._real_y(win)
        width = abs(self.p2._real_x(win) - self.p1._real_x(win))
        height = abs(self.p1._real_y(win) - self.p2._real_y(win))
        #fill
        if self.color != win.bgcolor and self.isFilled:
            pygame.draw.rect(win.screen, self.color, 
                (x, y, width, height), 0) 
        #outline
        pygame.draw.rect(win.screen, self.outline, 
            (x, y, width, height), 
            self.thickness)

    def getP1(self):
        return self.p1

    def getP2(self):
        return self.p2


class Oval(Rectangle):
    def _update(self, win):
        x = self.p1._real_x(win)
        y = self.p2._real_y(win)
        width = abs(self.p2._real_x(win) - self.p1._real_x(win))
        height = abs(self.p1._real_y(win) - self.p2._real_y(win))
        #fill
        if self.color != win.bgcolor:
            pygame.draw.ellipse(win.screen, self.color, 
                (x, y, width, height), 0) 
        #outline
        pygame.draw.ellipse(win.screen, self.outline, 
            (x, y, width, height), 
            self.thickness)


class Circle(Drawable):
    def __init__(self, p, radius):
        super().__init__()
        self.rad = radius
        self.p = p

    def setFill(self, c):
        self.color = _color(c)
    
    def getCenter(self):
        return self.p
    
    def getRadius(self):
        return self.rad

    def _update(self, win):
        x = self.p._real_x(win)
        y = self.p._real_y(win)
        #fill
        if self.color != win.bgcolor:
            pygame.draw.circle(win.screen, self.color, 
                (x, y), self.rad, 0) 
        #outline
        pygame.draw.circle(win.screen, self.outline, 
            (x, y), self.rad,
            self.thickness)


class GraphWin:
    def __init__(self, title, width, height, autoflush=True, icon=None):
        self.width = width
        self.height = height
        self.coord_system = False
        self.title = title
        self._objects = []
        self.bgcolor = (230, 230, 230)
        self.mouse_x = None
        self.mouse_y = None
        self.open = True
        self.autoflush = autoflush

        def event_loop():
            pygame.init()
            clock = pygame.time.Clock()

            pygame.display.set_caption(self.title)
            if icon:
                sur = pygame.image.load(icon)
                pygame.display.set_icon(sur)
            self.screen = pygame.display.set_mode(
                (self.width, self.height))
            self.screen.fill(self.bgcolor)
            pygame.display.update()
            while self.open:
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONUP:
                        pos = pygame.mouse.get_pos()
                        self.mouse_x = pos[0]
                        self.mouse_y = self.height - pos[1]
                        #time.sleep(0.1)
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        break
                self.screen.fill(self.bgcolor)
                for obj in self._objects:
                    obj._update(self)
                if self.autoflush:
                    pygame.display.update()
                clock.tick(frames_per_second)

        threading.Thread(target=event_loop).start()
        time.sleep(1)

    def _add_object(self, o):
        if o in self._objects:
            raise Exception("Object already drawn")
        self._objects.append(o)

    def _rem_object(self, o):
        if o in self._objects:
            self._objects.remove(o)

    def getMouse(self):
        mx, my = None, None
        while True:
            if self.mouse_x is not None and self.mouse_y is not None:
                mx, my = self.mouse_x, self.mouse_y
                break
            time.sleep(0.05)
        self.mouse_x = None
        self.mouse_y = None
        return Point(mx, my)

    def checkMouse(self):
        if self.mouse_x is not None and self.mouse_y is not None:
            self.mouse_x = None
            self.mouse_y = None
            mx, my = self.mouse_x, self.mouse_y
            return Point(mx, my)

    def plot(self, x, y, color):
        _Pixel(x, y, color).draw(self)

    def plotPixel(self, x, y, color):
        _Pixel(x, y, color, True).draw(self)

    def setBackground(self, c):
        self.bgcolor = _color(c)

    def setCoords(self, xll, yll, xur, yur):
        self.coord_system = True
        self.xll = xll
        self.yll = yll
        self.xur = xur
        self.yur = yur
    
    def close(self):
        self.open = False
        pygame.quit()


def update(t=None):
    global frames_per_second
    pygame.display.update()
    if t is not None:
        frames_per_second = t


if __name__ == "__main__":
    g = GraphWin("Test", 640, 480)
    r = Rectangle(Point(100, 100), Point(150, 150))
    r.draw(g)
    while True:
        g.getMouse()
        r.setFill("red")