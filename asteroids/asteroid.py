# Author: Jonathan Jengo

import math
from random import randint, random
from .sprite import Sprite
from .util import Point, ScreenSize

class Asteroid(Sprite):
    
    # Various sizes
    Small, Medium, Large = range(3)
    
    # Initialize
    def __init__(self, size = Large):
        Sprite.__init__(self)
        self.thetaVel = 0.0
        self.speed = 0.35
        self.size = size
        self.initShape()
        self.initMotion()
        self.initEdge()
    
    # Generate a randomized shape
    def initShape(self):

        sides = randint(8, 12)
        xpts, ypts = [], []
        
        # Create vertices with random edges and angles
        for i in range(sides):
            
            sidelen = (random() * 20.0 + 15) + 12
            if self.size == Asteroid.Medium:
                sidelen /= 2
            elif self.size == Asteroid.Small:
                sidelen /= 4
            
            theta = 2.0 * math.pi / sides * i
            xpts.append(-round(sidelen * math.sin(theta)))
            ypts.append(round(sidelen * math.cos(theta)))
        
        self.setPoints(xpts, ypts, True)

    # Generate random motion
    def initMotion(self):
        
        self.thetaVel = ((random() - 0.5) / 10.0) * self.speed
        self.vel.x = random() * randint(2, 4) * self.speed
        self.vel.y = random() * randint(2, 4) * self.speed
        
        if random() < 0.5:
            self.vel.x = -self.vel.x            
        if random() < 0.5:
            self.vel.y = -self.vel.y
            
    # Generate random edge location
    def initEdge(self):
        
        side = randint(0, 3)
        
        if side == 0:
            self.pos = Point(25, random() * ScreenSize[1])
        elif side == 1:
            self.pos = Point(ScreenSize[0] - 25, random() * ScreenSize[1])
        elif side == 2:
            self.pos = Point(random() * ScreenSize[0], 25)
        else:
            self.pos = Point(random() * ScreenSize[0], ScreenSize[1] - 25)

    # Split off into smaller asteroids
    def split(self):
        
        pieces = []
        
        if self.size != Asteroid.Small:
            for i in range(3):
                a = Asteroid(self.size - 1)
                a.pos.x = self.pos.x
                a.pos.y = self.pos.y
                a.vel.x *= 2.0
                a.vel.y *= 2.0
                pieces.append(a)
            
        return pieces
    
    # Destroyed score value
    def scoreValue(self):
        if self.size == Asteroid.Small:
            return 100
        elif self.size == Asteroid.Medium:
            return 50
        else:
            return 20