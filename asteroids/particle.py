import pygame
from random import randint
from asteroids.util import Point

class Particles(object):
    
    def __init__(self):
        self.particles = []
        
    # Create random particles from a range of [x,y] points
    def generate_particles(self, pts):
        for i in xrange(int(len(pts) / 4)):
            pt = pts[randint(0, len(pts) - 1)]
            self.particles.append(Particle(pt))
            pts.remove(pt)
            
    # Update all particles
    def update(self):
        self.particles[:] = [p for p in self.particles if p.alive]
        for particle in self.particles:
            particle.update()

    # Render fading particles
    def render(self, gfx):
        for particle in self.particles:
            particle.render(gfx)

class Particle(object):
    
    def __init__(self, pos):
        self.pos = Point(pos.x, pos.y)
        self.vel = Point(0.0, 0.0)
        self.color = [255, 255, 255]
        self.fade = 10
        self.alive = True
        
    # Update particle values
    def update(self):
        self.pos.x += self.vel.x
        self.pos.y += self.vel.y
        self.color = [col - self.fade for col in self.color]
        if self.color[0] < 0:
            self.alive = False
    
    # Render particle
    def render(self, gfx):
        if self.alive:
            pygame.draw.aaline(gfx, self.color, (self.pos.x, self.pos.y), (self.pos.x, self.pos.y), 1)
