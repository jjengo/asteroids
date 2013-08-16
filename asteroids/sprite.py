# Author: Jonathan Jengo

import math
import pygame
from random import random
from . import util

# Represents a [x,y] coordinate
class Point:
    
    # Initialize
    def __init__(self, x, y):
        self.x = x;
        self.y = y

    # Move coords to x,y
    def move(self, x, y):
        self.x = x;
        self.y = y
        
    # Move coords by dx,dy
    def translate(self, dx, dy):
        self.x += dx
        self.y += dy
        
# A sprite composed of connected vertices
class Sprite:
    
    # Initialize
    def __init__(self):
        self.pos = Point(0.0, 0.0)
        self.vel = Point(0.0, 0.0)
        self.theta = 0.0
        self.thetaVel = 0.0
        self.radius = 0.0
        self.orig = []
        self.pts = []
        self.alive = True
        self.wrap = Point(True, True)
        
    # Set points and calculate radius
    def setPoints(self, pts):
        
        self.orig = []
        self.orig.extend(pts)
            
        # Calculate bounding circle radius
        for pt in self.orig:
            dist = math.sqrt((pt.x ** 2) + (pt.y ** 2))
            if dist > self.radius:
                self.radius = dist
    
    # Move to location x,y
    def move(self, x, y):
        self.pos.move(x, y)
    
    # Move location by dx,dy
    def translate(self, dx, dy):
        self.pos.translate(dx, dy)
        
    # Scale points to a size [0.0 - 1.0]
    def scale(self, ratio):
        pts = [Point(pt.x * ratio, pt.y * ratio) for pt in self.orig]
        self.setPoints(pts)
            
    # Rotate angle by dt
    def rotate(self, dt):
        self.theta += dt
        if self.theta < 0:
            self.theta += 2.0 * math.pi
        if self.theta > (2.0 * math.pi):
            self.theta -= 2.0 * math.pi
            
    # Return if vertices create a closed polygon
    def isPolygon(self):
        if len(self.pts) > 1:
            return self.pts[0].x == self.pts[-1].x and self.pts[0].y == self.pts[-1].y
        else:
            return False
            
    # Use ray casting from inside the polygon to determine containment. 
    def contains(self, pt):
        
        # Even # of edge crossings = outside polygon
        # Odd # of edge crossing = inside polygon
        
        n = len(self.pts)
        inside = False
        p1 = Point(self.pts[0].x, self.pts[0].y)

        # Count edge crossings by casting a ray from inside the polygon     
        for i in range(n + 1):
            p2 = self.pts[i % n]

            if pt.y > min(p1.y, p2.y) and pt.y <= max(p1.y, p2.y) and pt.x <= max(p1.x, p2.x):
                if p1.y != p2.y:
                    xinters = (pt.y - p1.y) * (p2.x - p1.x) / (p2.y - p1.y) + p1.x
                if p1.x == p2.x or pt.x <= xinters:
                    inside = not inside
            p1.x, p1.y = p2.x, p2.y        
        
        return inside

    # Checks if the polygon contains any sprite vertices            
    def collision(self, sprite):
        
        # Only polygons can collide
        if not self.isPolygon() or not sprite.isPolygon():
            return False
    
        # Only check if in close proximity
        if not self.proximity(sprite):
            return False
        
        # First check if this polygon contains any vertex
        for pt in sprite.pts:
            if self.contains(pt):
                return True
            
        # Next check sprite polygon against current vertices
        for pt in self.pts:
            if sprite.contains(pt):
                return True
            
        return False

    # Use pythagorean theorem to check proximmity distance
    def proximity(self, s, dist = 55):
        a2 = (s.pos.x - self.pos.x) ** 2
        b2 = (s.pos.y - self.pos.y) ** 2
        return math.sqrt(a2 + b2) < dist

    # Update all coordinate values
    def update(self):
        
        # Update position based on velocity
        self.pos.x += self.vel.x
        self.pos.y += self.vel.y
        
        # Update angle based on velocity
        self.rotate(self.thetaVel)
        
        # Wrap position within screen bounds
        if self.wrap.x:
            self.pos.x = util.wrapX(self.pos.x, self)
        if self.wrap.y:
            self.pos.y = util.wrapY(self.pos.y, self)
        
        # Update vertices based on pos and angle
        self.pts = []
        for pt in self.orig:
            newx = (pt.x * math.cos(self.theta)) - (pt.y * math.sin(self.theta)) + self.pos.x
            newy = (pt.x * math.sin(self.theta)) + (pt.y * math.cos(self.theta)) + self.pos.y
            self.pts.append(Point(newx, newy))
            
    # Draw to the display
    def render(self, gfx, color = [255, 255, 255]):
        for start, end in zip(self.pts[:-1], self.pts[1:]):
            pygame.draw.aaline(gfx, color, (start.x, start.y), (end.x, end.y), 1)
        
# A sprite explosion composed of sprite edges
class Explosion:
    
    # Initialize
    def __init__(self, sprite):
    
        self.color = [255, 255, 255]
        self.fade = 15
        self.alive = True
        self.sides = []
        
        for start, end in zip(sprite.orig[1:], sprite.orig[:-1]):
            side = Sprite()
            side.orig = [start, end]
            side.pos = Point(sprite.pos.x, sprite.pos.y)
            side.vel = Point((random() * 4) - 2, (random() * 4) - 2)
            side.theta = sprite.theta
            self.sides.append(side)
        
    # Update all the values
    def update(self):
        
        for side in self.sides:
            side.update()
        
        self.color[0] -= self.fade
        self.color[1] -= self.fade
        self.color[2] -= self.fade
        if self.color[0] <= 0:
            self.alive = False
            
    # Render the fading sides
    def render(self, gfx):
        for side in self.sides:
            side.render(gfx, self.color)
             