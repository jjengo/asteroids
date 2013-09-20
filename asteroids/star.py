#!/usr/bin/env python3

from random import randint
from .sprite import Sprite, Point
from .util import ScreenSize

# A flickering star
class Star(Sprite):
    
    # Initialize
    def __init__(self, bounds):
        Sprite.__init__(self)
        self.pos.x = randint(bounds.pos.x, bounds.pos.x + bounds.size.width - 1)
        self.pos.y = randint(bounds.pos.y, bounds.pos.y + bounds.size.height - 1)
        self.color =[255, 255, 255]
        self.fade = 10
        self.timeToFade = randint(25, 500)
        self.initShape()
    
    # Initialize the shape    
    def initShape(self):
        pts = [Point(x, y) for x, y in zip([0, 0, 1, 1, 0], [0, 1, 1, 0, 0])]
        self.setPoints(pts)
        
    # Update all values
    def update(self):
        Sprite.update(self)
        if self.timeToFade:
            self.timeToFade -= 1
        else:
            col = self.color[0] - self.fade
            if col >= 255:
                self.timeToFade = randint(25, 100)
                col = 255
            elif col <= 0:
                col = 0
            if not col or col == 255:
                self.fade *= -1
            self.color = [col, col, col]
            
    # Render the fading star
    def render(self, gfx):
        if self.alive:
            Sprite.render(self, gfx, self.color)
            
    # More efficient collision detection by only checking origin point.
    def collision(self, sprite):
        if not sprite.isPolygon() or not self.proximity(sprite):
            return False
        else:
            return sprite.contains(self.pts[0])
    