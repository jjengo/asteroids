import sys
import pygame
from pygame.locals import *
from random import randint
from asteroids.game import Asteroids
from asteroids.asteroid import Asteroid
from asteroids.util import ScreenSize
        
class Core(object):
    
    # Various game states
    Menu, Running, Paused, GameOver = xrange(4)
    
    # Initialize
    def __init__(self, gfx):
        self.gfx = gfx
        self.keys = {}
        self.menu = Menu()
        self.game = Asteroids()
        self.state = self.Menu
        self.time_to_menu = 0
                
    # Run core engine
    def run(self):
        
        clock = pygame.time.Clock()
                
        while True:
            
            for event in pygame.event.get():
                self.handle_event(event)

            self.gfx.fill((0, 0, 0))
            
            # Game State: Menu
            if self.state == self.Menu:
                self.menu.update()
                self.menu.render(self.gfx)
                
            # Game State: Running
            elif self.state == self.Running:
                self.game.process_key_events(self.keys)
                self.game.update()
                self.game.render(self.gfx)
                
            # Game State: Paused
            elif self.state == self.Paused:
                self.game.render(self.gfx)
                
            # Game State: Game Over
            elif self.state == self.GameOver:
                self.game.update()
                self.game.render(self.gfx)

            self.process_key_events()
            self.update()
            self.render(self.gfx)
            
            pygame.display.update()
            clock.tick(30)
            
    # Handle caught pygame event
    def handle_event(self, event):
        
        # Handle exit events.
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
            
        # Handle key events.
        elif event.type == KEYDOWN:
            self.keys[event.key] = True
        elif event.type == KEYUP:
            self.keys[event.key] = False

    # Process all relevant key events
    def process_key_events(self):
        
        if self.keys.get(K_RETURN, False):
            if self.state == self.Menu:
                self.state = self.Running
                self.game.new_game()
                
        if self.keys.get(K_p, False):
            if self.state == self.Running:
                self.state = self.Paused
                self.game.mixer.pause()
            elif self.state == self.Paused:
                self.state = self.Running
                self.game.mixer.unpause()
            self.keys[K_p] = False
            
    # Update values
    def update(self):

        if self.state == self.Running:
            if self.game.game_over():
                self.game.mixer.stopall()
                self.state = self.GameOver
                self.time_to_menu = 200
        elif self.state == self.GameOver:
            self.time_to_menu -= 1
            if self.time_to_menu == 0:
                self.state = self.Menu
        
    # Render values
    def render(self, gfx):
        
        font = pygame.font.SysFont("OCR A Extended", 20)
        
        if self.state == self.Paused:
            label = font.render("Paused", 1, (255, 255, 255))
            gfx.blit(label, ((ScreenSize.width / 2) - (label.get_rect().width / 2), 190))
        elif self.state == self.GameOver:
            label = font.render("Game Over", 1, (255, 255, 255))
            gfx.blit(label, ((ScreenSize.width / 2) - (label.get_rect().width / 2), 190))
        
class Menu(object):
    
    def __init__(self):
        self.asteroids = []
        for i in xrange(10):
            size = randint(0, 2)
            self.asteroids.append(Asteroid(size))
    
    # Update all values
    def update(self):
        for asteroid in self.asteroids:
            asteroid.update()
    
    # Render sprites
    def render(self, gfx):
        
        for asteroid in self.asteroids:
            asteroid.render(gfx)
    
        font = pygame.font.SysFont("OCR A Extended", 50)
        label = font.render("ASTEROIDS", 1, (255, 255, 255))
        gfx.blit(label, ((ScreenSize.width / 2) - (label.get_rect().width / 2), 75))
    
        font = pygame.font.SysFont("OCR A Extended", 20)
        label = font.render("Play Game", 1, (255, 255, 255))
        gfx.blit(label, ((ScreenSize.width / 2) - (label.get_rect().width / 2), 200))

        font = pygame.font.SysFont("OCR A Extended", 12)
        label = font.render("Jonathan Jengo", 1, (255, 255, 255))
        gfx.blit(label, ((ScreenSize.width / 2) - (label.get_rect().width / 2), 375))
