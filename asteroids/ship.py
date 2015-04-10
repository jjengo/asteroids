import math
from asteroids.sprite import Sprite
from asteroids.util import Point

class Ship(Sprite):
    
    def __init__(self):
        Sprite.__init__(self)
        self.speed = 0.27
        self.decay = 0.98
        self.pos = Point(350, 200)
        self.time_to_respawn = 0
        self.init_shape()
        
    @property
    def front(self):
        return self.pts[0]
    
    def init_shape(self):
        xpts = [0, -7, 7]
        ypts = [-10, 10, 10]
        self.set_points(xpts, ypts, True)
        
    def update(self):
        
        Sprite.update(self)
        self.vel.x *= self.decay
        self.vel.y *= self.decay
        
        # Countdown to respawn
        if self.time_to_respawn > 0:
            self.time_to_respawn -= 1
            if self.time_to_respawn == 0:
                self.alive = True
    
    # Move in the direction pointed
    def forward_thrust(self):
        self.vel.x += math.sin(self.theta) * self.speed
        self.vel.y -= math.cos(self.theta) * self.speed
        
    # Reverse in the direction pointed
    def backward_thrust(self):
        self.vel.x -= math.sin(self.theta) * self.speed
        self.vel.y += math.cos(self.theta) * self.speed
        
    # Rotate clockwise
    def rotate_right(self):
        self.rotate(math.pi / 18.0)

    # Rotate counter clockwise
    def rotate_left(self):
        self.rotate(-math.pi / 18.0)
        
    # Return a list of ranges for the vapor bounds
    def vapor_bounds_range(self):

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
    def fire_bullet(self):
        bullet = Bullet(self.front.x, self.front.y, self.theta)
        bullet.from_ship = True
        return bullet
    
    # Start respawn process
    def respawn(self):
        self.time_to_respawn = 100
        self.pos = Point(350, 200)
        self.vel = Point(0, 0)
        
class Bullet(Sprite):
    
    def __init__(self, x, y, theta):
        Sprite.__init__(self)
        self.pos.x = x
        self.pos.y = y
        self.theta = theta
        self.vel.x = math.sin(theta) * 10.0
        self.vel.y = -math.cos(theta) * 10.0
        self.time_to_live = 30
        self.from_ship = False
        self.init_shape()
        
    # Initialize the shape
    def init_shape(self):
        xpts = [0, 0, 1, 1]
        ypts = [0, 1, 1, 0]
        self.set_points(xpts, ypts, True)

    # Update all values
    def update(self):
        Sprite.update(self)
        self.time_to_live -= 1
        if self.time_to_live <= 0:
            self.alive = False
        