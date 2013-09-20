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
        self.timeToFade = randint(25, 250)
        self.initShape()
    
    # Initialize the shape    
    def initShape(self):
        xpts = [0, 0, 1, 1]
        ypts = [0, 1, 1, 0]
        self.setPoints(xpts, ypts, True)

    # Update all values
    def update(self):
        
        Sprite.update(self)
        
        if self.timeToFade:
            self.timeToFade -= 1
        else:
            self.color = [col - self.fade for col in self.color]
            if self.color[0] >= 255:
                self.timeToFade = randint(25, 250)
                self.color = [255, 255, 255]
                self.fade *= -1
            elif self.color[0] <= 0:
                self.color = [0, 0, 0]
                self.fade *= -1

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
    