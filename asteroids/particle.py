# Author: Jonathan Jengo

import math
import pygame
from random import randint
from .sprite import Point

# Engine to create various particle effects
class Particles:
    
    # Initialize
    def __init__(self):
        self.particles = []
        
    # Create a single particle
    def createParticle(self, pt):
        self.particles.append(Particle(pt))
        
    # Create random particles from a range of [x,y] points
    def createRandomParticles(self, pts):
        
        for i in range(int(len(pts) / 4)):
            pt = pts[randint(0, len(pts) - 1)]
            self.particles.append(Particle(pt))
            pts.remove(pt)
            
    # Create an expanding circle of particles
    def createParticleRing(self, pt):
        
        for angle in range(360):
            theta = math.radians(angle)
            p = Particle(pt)
            p.vel = Point(-math.sin(theta) * 5.0, math.cos(theta) * 5.0)
            self.particles.append(p)

    # Update all particles
    def update(self):
        self.particles[:] = [p for p in self.particles if p.alive]
        for particle in self.particles:
            particle.update()

    # Render fading particles
    def render(self, gfx):
        for particle in self.particles:
            particle.render(gfx)

# A particle with position, velocity, and fade
class Particle:
    
    # Initalize
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