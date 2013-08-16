# Author: Jonathan Jengo

import sys
import pygame
from pygame.locals import *
from random import randint
from . import sound as Sound
from .sprite import Explosion
from .ship import Ship, Bullet
from .asteroid import Asteroid
from .saucer import Saucer
from .particle import Particles
from .sound import Mixer
from .util import Keys, ScreenSize
        
# Core engine
class Core:
    
    # Various game states
    Menu, Running, Paused, GameOver = range(4)
    
    # Initialize
    def __init__(self, gfx):
        self.gfx = gfx
        self.keys = Keys()
        self.menu = Menu()
        self.game = Asteroids()
        self.state = Core.Menu
        self.timeToMenu = 0
                
    # Run core engine
    def run(self):
        
        clock = pygame.time.Clock()
                
        while True:
            
            for event in pygame.event.get():
                self.handleEvent(event)

            self.gfx.fill((0, 0, 0))
            
            # Game State: Menu
            if self.state == Core.Menu:
                self.menu.update()
                self.menu.render(self.gfx)
                
            # Game State: Running
            elif self.state == Core.Running:
                self.game.processKeyEvents(self.keys)
                self.game.update()
                self.game.render(self.gfx)
                
            # Game State: Paused
            elif self.state == Core.Paused:
                self.game.render(self.gfx)
                
            # Game State: Game Over
            elif self.state == Core.GameOver:
                self.game.update()
                self.game.render(self.gfx)

            self.processKeyEvents()
            self.update()
            self.render(self.gfx)
            
            pygame.display.update()
            clock.tick(30)
            
    # Handle caught pygame event
    def handleEvent(self, event):
        
        # Handle exit events.
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
            
        # Handle key events.
        elif event.type == KEYDOWN:
            self.keys.put(event.key, True)
        elif event.type == KEYUP:
            self.keys.put(event.key, False)

    # Process all relevant key events
    def processKeyEvents(self):
        
        if self.keys.isKeyDown(K_RETURN):
            if self.state == Core.Menu:
                self.state = Core.Running
                self.game.newGame()
                
        if self.keys.isKeyDown(K_p):
            if self.state == Core.Running:
                self.state = Core.Paused
                self.game.mixer.pause()
            elif self.state == Core.Paused:
                self.state = Core.Running
                self.game.mixer.unpause()
            self.keys.put(K_p, False)
            
    # Update values
    def update(self):

        if self.state == Core.Running:
            if self.game.gameOver():
                self.game.mixer.stopall()
                self.state = Core.GameOver
                self.timeToMenu = 200
        elif self.state == Core.GameOver:
            self.timeToMenu -= 1
            if self.timeToMenu == 0:
                self.state = Core.Menu
        
    # Render values
    def render(self, gfx):
        
        font = pygame.font.SysFont("OCR A Extended", 20)
        
        if self.state == Core.Paused:
            label = font.render("Paused", 1, (255, 255, 255))
            gfx.blit(label, ((ScreenSize[0] / 2) - (label.get_rect().width / 2), 190))
        elif self.state == Core.GameOver:
            label = font.render("Game Over", 1, (255, 255, 255))
            gfx.blit(label, ((ScreenSize[0] / 2) - (label.get_rect().width / 2), 190))

# Asteroids game engine
class Asteroids:
    
    # Initialize
    def __init__(self):
        self.stats = Statistics()
        self.mixer = Mixer()
        self.particles = Particles()
        self.ship = Ship()
        self.bullets = []
        self.asteroids = []
        self.saucers = []
        self.explosions = []
        self.timeToLevel = 0
        self.saucerElapsed = 0
        
    # Process key state events
    def processKeyEvents(self, keys):
        
        if self.ship.alive:
            
            # Ship thrust
            if keys.isKeyDown(K_UP):
                self.ship.forwardThrust()
                self.emitVaporTrail()
                self.mixer.loop(Sound.Thrust)
            elif keys.isKeyDown(K_DOWN):
                self.ship.backwardThrust()
            
            # Ship rotation
            if keys.isKeyDown(K_LEFT):
                self.ship.rotateLeft()
            elif keys.isKeyDown(K_RIGHT):
                self.ship.rotateRight()
                        
            # Fire bullet
            if keys.isKeyDown(K_SPACE):
                self.fireShipBullet()
                keys.put(K_SPACE, False)

            # Stop thrust
            if not keys.isKeyDown(K_UP):
                self.mixer.stop(Sound.Thrust)
                
    # Update all sprites
    def update(self):
            
        self.checkCollisions()
        self.mixer.update()
        self.particles.update()        
        self.ship.update()
        
        # Update bullets
        self.bullets[:] = [b for b in self.bullets if b.alive]
        for bullet in self.bullets:
            bullet.update()
                
        # Update asteroids
        self.asteroids[:] = [a for a in self.asteroids if a.alive]
        for asteroid in self.asteroids:
            asteroid.update()
            
            # Avoid asteroids in close proximity
            for saucer in self.saucers:
                if saucer.proximity(asteroid, asteroid.radius * 3):
                    saucer.avoid(asteroid)
                    break

        # Update saucers
        if self.timeForSaucer():
            self.spawnSaucer()
        self.saucers[:] = [s for s in self.saucers if s.alive]
        for saucer in self.saucers:
            saucer.update()
            if not saucer.alive:
                self.mixer.stopLiveSaucer(saucer)
            elif saucer.timeToFire < 0:
                self.fireSaucerBullet(saucer)
        
        # Update explosions
        self.explosions[:] = [e for e in self.explosions if e.alive]
        for explosion in self.explosions:
            explosion.update()
            
        # Check for earned extra life        
        if self.stats.earnedLife():
            self.stats.extras += 1
            self.stats.ships += 1
            self.mixer.play(Sound.Extra, 5)
    
        # Countdown to next level
        if self.levelComplete():
            if self.timeToLevel > 0:
                self.timeToLevel -= 1
                if self.timeToLevel == 0:
                    self.nextLevel()
            elif self.timeToLevel == 0:
                self.timeToLevel = 100
                self.mixer.stop(Sound.Music)
 
    # Render all sprites
    def render(self, gfx):

        self.stats.render(gfx)
        self.particles.render(gfx)
        if self.ship.alive:
            self.ship.render(gfx)
        for sprite in self.bullets + self.asteroids + self.saucers + self.explosions:
            sprite.render(gfx)

    # Check sprite collisions
    def checkCollisions(self):        
                
        # Asteroid collisions
        for asteroid in self.asteroids:
            
            # Asteroid/Ship collisions
            if self.ship.alive and asteroid.collision(self.ship):
                self.shipDestroyed()
            
            # Asteroid/Saucer collisions
            for saucer in self.saucers:
                if saucer.collision(asteroid):
                    self.saucerDestroyed(saucer)
                
            # Asteroid/Bullet collisions
            for bullet in self.bullets:
                if bullet.collision(asteroid):
                    self.asteroidDestroyed(asteroid)
                    bullet.alive = False
                    if bullet.fromShip:
                        self.stats.score += asteroid.scoreValue()
                        self.stats.destroyed += 1
        
        # Bullet collisions
        for bullet in self.bullets:
            
            # Bullet/Ship collision
            if self.ship.alive and bullet.collision(self.ship):
                self.shipDestroyed()
                
            # Bullet/Saucer collisions
            for saucer in self.saucers:
                if bullet.collision(saucer):
                    self.saucerDestroyed(saucer)
                    bullet.alive = False
                    if bullet.fromShip:
                        self.stats.score += saucer.scoreValue()
                        self.stats.destroyed += 1
        
        # Saucer/Ship collisions
        for saucer in self.saucers:
            if self.ship.alive and saucer.collision(self.ship):
                self.shipDestroyed()

    # Fire a bullet in the direction the ship is pointing
    def fireShipBullet(self):
        if len([b for b in self.bullets if b.fromShip]) < 5:
            bullet = self.ship.fireBullet()
            self.bullets.append(bullet)
            self.mixer.play(Sound.Fire)
            self.stats.fired += 1
    
    # Fire a bullet from a saucer
    def fireSaucerBullet(self, saucer):
        bullet = saucer.fireBullet(self.ship.pos)
        self.bullets.append(bullet)
    
    # Create a vapor trail behind the moving ship
    def emitVaporTrail(self):
        bounds = self.ship.getVaporBoundsRange()
        for pts in bounds:
            self.particles.createRandomParticles(pts)

    # Kill ship and explode
    def shipDestroyed(self):
        self.explosions.append(Explosion(self.ship))
        self.mixer.stop(Sound.Thrust)
        self.mixer.play(Sound.MediumBang)
        self.stats.ships -= 1
        self.ship.alive = False
        if not self.gameOver():
            self.ship.respawn()
    
    # Kill asteroid and explode
    def asteroidDestroyed(self, asteroid):
        self.explosions.append(Explosion(asteroid))
        self.asteroids.extend(asteroid.split())
        self.mixer.playAsteroidBang(asteroid)
        asteroid.alive = False
    
    # Kill saucer and explode
    def saucerDestroyed(self, saucer):
        self.explosions.append(Explosion(saucer))
        self.mixer.stopLiveSaucer(saucer)
        self.mixer.playSaucerBang(saucer)
        saucer.alive = False
        
    # Def spawn a new saucer
    def spawnSaucer(self):
        if randint(1, 7) < self.stats.level:
            self.saucers.append(Saucer(Saucer.Small))
            self.mixer.loop(Sound.SmallSaucer)
        else:
            self.saucers.append(Saucer(Saucer.Large))
            self.mixer.loop(Sound.LargeSaucer)
            
    # Return if time for a saucer
    def timeForSaucer(self):

        if self.gameOver():
            return False
        
        self.saucerElapsed += 1
        factor = 800 - self.saucerElapsed
        factor += randint(0, len(self.asteroids) * 5)
        factor -= randint(0, self.stats.level * 50)
        if (factor < 0):
            self.saucerElapsed = 0
            
        return factor < 0
    
    # Start a new game
    def newGame(self):
        self.stats = Statistics()
        self.asteroids = []
        self.saucers = []
        self.bullets = []
        self.ship = Ship()
        self.saucerElapsed = 0
        self.nextLevel()

    # Start the next level
    def nextLevel(self):
        self.stats.level += 1
        for i in range(self.stats.level + 2):
            self.asteroids.append(Asteroid())
        self.mixer.play(Sound.Music)

    # Return if the level is complete
    def levelComplete(self):
        return len(self.asteroids) == 0 and len(self.saucers) == 0
    
    # Return if the game is over
    def gameOver(self):
        return self.stats.ships == 0
    
# Game statistics
class Statistics:
    
    # Initialize
    def __init__(self):
        self.ships = 3
        self.score = 0
        self.level = 0
        self.fired = 0
        self.destroyed = 0
        self.extras = 0
        
    # Render statistic values
    def render(self, gfx):
        
        # Score
        font = pygame.font.SysFont("OCR A Extended", 16)
        label = font.render(repr(self.score), 1, (255, 255, 255))
        gfx.blit(label, (10, 10))
        
        # Ships
        for i in range(self.ships):
            ship = Ship()
            ship.pos.x = (i * 16) + 14
            ship.pos.y = 40
            ship.scale(0.75)
            ship.update()
            ship.render(gfx)
            
    # Return if earned extra life
    def earnedLife(self):
        return (self.score - (self.extras * 10000)) > 10000
        
# Start menu
class Menu:
    
    # Initialize
    def __init__(self):
        self.asteroids = []
        for i in range(10):
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
        gfx.blit(label, ((ScreenSize[0] / 2) - (label.get_rect().width / 2), 75))
    
        font = pygame.font.SysFont("OCR A Extended", 20)
        label = font.render("Play Game", 1, (255, 255, 255))
        gfx.blit(label, ((ScreenSize[0] / 2) - (label.get_rect().width / 2), 200))

        font = pygame.font.SysFont("OCR A Extended", 12)
        label = font.render("Jonathan Jengo", 1, (255, 255, 255))
        gfx.blit(label, ((ScreenSize[0] / 2) - (label.get_rect().width / 2), 375))
