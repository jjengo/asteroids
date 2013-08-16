# Author: Jonathan Jengo

import math
from .sprite import Sprite, Point

# The user spaceship
class Ship(Sprite):
    
    # Initialize
    def __init__(self):
        Sprite.__init__(self)
        self.speed = 0.27
        self.decay = 0.98
        self.pos = Point(350, 200)
        self.timeToRespawn = 0
        self.initShape()
        
    # Initialize the ship shape
    def initShape(self):
        pts = []
        pts.append(Point(0, -10))
        pts.append(Point(-7, 10))
        pts.append(Point(7, 10))
        pts.append(pts[0])
        self.setPoints(pts)

    # Update all the values
    def update(self):
        
        Sprite.update(self)
        self.vel.x *= self.decay
        self.vel.y *= self.decay
        
        # Countdown to respawn
        if self.timeToRespawn > 0:
            self.timeToRespawn -= 1
            if self.timeToRespawn == 0:
                self.alive = True
    
    # Move in the direction pointed
    def forwardThrust(self):
        self.vel.x += math.sin(self.theta) * self.speed
        self.vel.y -= math.cos(self.theta) * self.speed
        
    # Reverse in the direction pointed
    def backwardThrust(self):
        self.vel.x -= math.sin(self.theta) * self.speed
        self.vel.y += math.cos(self.theta) * self.speed
        
    # Rotate clockwise
    def rotateRight(self):
        self.rotate(math.pi / 18.0)

    # Rotate counter clockwise
    def rotateLeft(self):
        self.rotate(-math.pi / 18.0)
        
    # Return the front tip of the ship
    def getFront(self):
        return self.pts[0]

    # Return a list of ranges for the vapor bounds
    def getVaporBoundsRange(self):

        bounds = []
        size = int(abs(self.vel.x) + abs(self.vel.y))
        if size < 6:
            size = 6
        
        for dy in range(size):
            
            pts = []
            gap = 3
            y = self.orig[1].y + dy
            
            for x in range(int(self.orig[1].x + gap), int(self.orig[2].x - gap), 1):
                newx = (x * math.cos(self.theta)) - (y * math.sin(self.theta)) + self.pos.x
                newy = (x * math.sin(self.theta)) + (y * math.cos(self.theta)) + self.pos.y
                pts.append(Point(newx, newy))
                
            bounds.append(pts)
        
        return bounds
    
    # Fire a directed bullet
    def fireBullet(self):
        bullet = Bullet(self.pts[0].x, self.pts[0].y, self.theta)
        bullet.fromShip = True
        return bullet
    
    # Start respawn process
    def respawn(self):
        self.timeToRespawn = 100
        self.pos = Point(350, 200)
        self.vel = Point(0, 0)
        
# Bullet fired from the spaceship
class Bullet(Sprite):
    
    #Initialize
    def __init__(self, x, y, theta):
        Sprite.__init__(self)
        self.pos.x = x
        self.pos.y = y
        self.theta = theta
        self.vel.x = math.sin(theta) * 10.0
        self.vel.y = -math.cos(theta) * 10.0
        self.timeToLive = 30
        self.fromShip = False
        self.initShape()
        
    # Initialize the shape
    def initShape(self):
        pts = []
        pts.append(Point(0, 0))
        pts.append(Point(0, 1))
        pts.append(Point(1, 1))
        pts.append(Point(1, 0))
        pts.append(pts[0])
        self.setPoints(pts)
    
    # Update all values
    def update(self):
        Sprite.update(self)
        self.timeToLive -= 1
        if self.timeToLive <= 0:
            self.alive = False
        