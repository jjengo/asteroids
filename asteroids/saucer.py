# Author: Jonathan Jengo

import math
import pygame
from random import randint, random
from .sprite import Sprite, Point
from .ship import Bullet
from .util import ScreenSize

class Saucer(Sprite):
    
    # Various sizes
    Small, Large = range(2)
    
    # Initialize
    def __init__(self, size = Large):
        Sprite.__init__(self)
        self.size = size
        self.wrap.x = False
        self.speed = 2.0
        self.timeToFire = 30
        self.initShape()
        self.initEdge()
        self.resetDeviation()
        
    # Generate the suacer shape
    def initShape(self):
        xpts = [-4, 4, 7, 15, 8, -8, -15, -7]
        ypts = [-9, -9, -3, 3, 9, 9, 3, -3]
        self.setPoints(xpts, ypts, True)
        if self.size == Saucer.Small:
            self.scale(0.6)
        
    # Generate random edge location and velocity
    def initEdge(self):
        
        if randint(0, 1):
            self.pos.x = self.orig[6].x + 1
            self.vel.x = (1 * self.speed)
        else:
            self.pos.x = ScreenSize[0] - self.orig[3].x - 1
            self.vel.x = (-1 * self.speed)
            
        self.pos.y = random() * ScreenSize[1]
        self.vel.y = 0
        
    # Update all values
    def update(self):
            
        Sprite.update(self)
        if self.pos.x < self.orig[6].x or self.pos.x > ScreenSize[0] + self.orig[3].x:
            self.alive = False
    
        self.timeToDeviate -=1
        if self.timeToDeviate <= 0:
            self.deviateCourse()
            self.resetDeviation()    
        self.timeToFire -= 1
                    
    # Render outline and details
    def render(self, gfx, color = [255, 255, 255]):
        Sprite.render(self, gfx)
        pygame.draw.aaline(gfx, color, (self.pts[2].x, self.pts[2].y), (self.pts[7].x, self.pts[7].y), 1)
        pygame.draw.aaline(gfx, color, (self.pts[3].x, self.pts[3].y), (self.pts[6].x, self.pts[6].y), 1)
        
    # Deviate off course
    def deviateCourse(self):
        curr = self.vel.y
        while self.vel.y == curr:
            self.vel.y = randint(-1, 1) * self.speed
            
    # Reset deviation timer
    def resetDeviation(self):
        self.timeToDeviate = randint(30, 100)
            
    # Change velocity to avoid sprite
    def avoid(self, sprite):
        if self.pos.y - sprite.pos.y > 0:
            self.vel.y = self.speed
        else:
            self.vel.y = -self.speed
        self.resetDeviation()
            
    # Fire a bullet toward a point
    def fireBullet(self, pt):
        
        self.timeToFire = 30
          
        # Fire bullet toward specific point
        if self.size == Saucer.Small:
            
            # Add a little bit of error
            dest = Point(pt.x, pt.y)
            dest.x += randint(-20, 20)
            dest.y += randint(-20, 20)

            # Calculate theta and velocity toward point
            theta = math.atan2(dest.x - self.pos.x, self.pos.y - dest.y)
            vel = Point(math.sin(theta) * 5.0, -math.cos(theta) * 5.0)
            return Bullet(self.pos.x + vel.x, self.pos.y + vel.y, theta)
    
        # Fire bullet in random direction
        else:
            theta = random() * (2.0 * math.pi)
            vel = Point(math.sin(theta) * 10.0, -math.cos(theta) * 10.0)
            return Bullet(self.pos.x + vel.x, self.pos.y + vel.y, theta)
           
    # Destroyed score value
    def scoreValue(self):
        if self.size == Saucer.Small:
            return 1000
        else:
            return 200