import pygame
from pygame.locals import *
from random import randint
from asteroids import sound as Sound
from asteroids.sound import Mixer
from asteroids.sprite import Explosion
from asteroids.ship import Ship
from asteroids.asteroid import Asteroid
from asteroids.saucer import Saucer
from asteroids.particle import Particles
from asteroids.star import Star
from asteroids.util import Dimension, Rectangle, ScreenSize

class Asteroids(object):
    
    def __init__(self):
        self.stats = Statistics()
        self.mixer = Mixer()
        self.particles = Particles()
        self.ship = Ship()
        self.bullets = []
        self.asteroids = []
        self.saucers = []
        self.explosions = []
        self.stars = []
        self.time_to_level = 0
        self.saucer_elapsed = 0
        
    # Process key state events
    def process_key_events(self, keys):
        
        if self.ship.alive:
            
            # Ship thrust
            if keys.get(K_UP, False):
                self.ship.forward_thrust()
                self.emit_vapor_trail()
                self.mixer.thrust.loop()
            elif keys.get(K_DOWN, False):
                self.ship.backward_thrust()
            
            # Ship rotation
            if keys.get(K_LEFT, False):
                self.ship.rotate_left()
            elif keys.get(K_RIGHT, False):
                self.ship.rotate_right()
                        
            # Fire bullet
            if keys.get(K_SPACE, False):
                self.fire_ship_bullet()
                keys[K_SPACE] = False

            # Stop thrust
            if not keys.get(K_UP, False):
                self.mixer.thrust.stop()
                
    # Update all sprites
    def update(self):
            
        self.check_collisions()
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
        if self.time_for_saucer():
            self.spawn_saucer()
        self.saucers[:] = [s for s in self.saucers if s.alive]
        for saucer in self.saucers:
            saucer.update()
            if not saucer.alive:
                self.mixer.stop_live_saucer(saucer)
            elif saucer.time_to_fire < 0:
                self.fire_saucer_bullet(saucer)
        
        # Update explosions
        self.explosions[:] = [e for e in self.explosions if e.alive]
        for explosion in self.explosions:
            explosion.update()
            
        # Update stars.
        for star in self.stars:
            star.update()
            
        # Check for earned extra life        
        if self.stats.earned_life():
            self.stats.extras += 1
            self.stats.ships += 1
            self.mixer.extra.play(5)
    
        # Countdown to next level
        if self.level_complete():
            if self.time_to_level > 0:
                self.time_to_level -= 1
                if self.time_to_level == 0:
                    self.next_level()
            elif self.time_to_level == 0:
                self.time_to_level = 100
                self.mixer.music.stop()
 
    # Render all sprites
    def render(self, gfx):

        self.stats.render(gfx)
        self.particles.render(gfx)
        if self.ship.alive:
            self.ship.render(gfx)
        for sprite in self.bullets + self.asteroids + self.saucers + self.explosions + self.stars:
            sprite.render(gfx)

    # Check sprite collisions
    def check_collisions(self):        
                
        # Asteroid collisions
        for asteroid in self.asteroids:
            
            # Asteroid/Ship collisions
            if self.ship.alive and asteroid.collision(self.ship):
                self.ship_destroyed()
            
            # Asteroid/Saucer collisions
            for saucer in self.saucers:
                if saucer.collision(asteroid):
                    self.saucer_destroyed(saucer)
                
            # Asteroid/Bullet collisions
            for bullet in self.bullets:
                if bullet.collision(asteroid):
                    self.asteroid_destroyed(asteroid)
                    bullet.alive = False
                    if bullet.from_ship:
                        self.stats.score += asteroid.score_value()
                        self.stats.destroyed += 1
        
        # Bullet collisions
        for bullet in self.bullets:
            
            # Bullet/Ship collision
            if self.ship.alive and bullet.collision(self.ship):
                self.ship_destroyed()
                
            # Bullet/Saucer collisions
            for saucer in self.saucers:
                if bullet.collision(saucer):
                    self.saucer_destroyed(saucer)
                    bullet.alive = False
                    if bullet.from_ship:
                        self.stats.score += saucer.score_value()
                        self.stats.destroyed += 1
        
        # Saucer/Ship collisions
        for saucer in self.saucers:
            if self.ship.alive and saucer.collision(self.ship):
                self.ship_destroyed()
                
        # Star collisions.
        for star in self.stars:
            star.alive = True
            for sprite in self.asteroids + self.saucers:
                if star.collision(sprite):
                    star.alive = False
                    break
            else:
                if star.collision(self.ship):
                    star.alive = False

    # Fire a bullet in the direction the ship is pointing
    def fire_ship_bullet(self):
        if len([b for b in self.bullets if b.from_ship]) < 5:
            bullet = self.ship.fire_bullet()
            self.bullets.append(bullet)
            self.mixer.fire.play()
            self.stats.fired += 1
    
    # Fire a bullet from a saucer
    def fire_saucer_bullet(self, saucer):
        bullet = saucer.fire_bullet(self.ship.pos)
        self.bullets.append(bullet)
    
    # Create a vapor trail behind the moving ship
    def emit_vapor_trail(self):
        bounds = self.ship.vapor_bounds_range()
        for pts in bounds:
            self.particles.generate_particles(pts)

    # Kill ship and explode
    def ship_destroyed(self):
        self.explosions.append(Explosion(self.ship))
        self.mixer.thrust.stop()
        self.mixer.medium_bang.play()
        self.stats.ships -= 1
        self.ship.alive = False
        if not self.game_over():
            self.ship.respawn()
    
    # Kill asteroid and explode
    def asteroid_destroyed(self, asteroid):
        self.explosions.append(Explosion(asteroid))
        self.asteroids.extend(asteroid.split())
        self.mixer.play_asteroid_bang(asteroid)
        asteroid.alive = False
    
    # Kill saucer and explode
    def saucer_destroyed(self, saucer):
        self.explosions.append(Explosion(saucer))
        self.mixer.stop_live_saucer(saucer)
        self.mixer.play_saucer_bang(saucer)
        saucer.alive = False
        
    # Def spawn a new saucer
    def spawn_saucer(self):
        if randint(1, 7) < self.stats.level:
            self.saucers.append(Saucer(Saucer.Small))
            self.mixer.small_saucer.loop()
        else:
            self.saucers.append(Saucer(Saucer.Large))
            self.mixer.large_saucer.loop()
            
    # Return if time for a saucer
    def time_for_saucer(self):

        if self.game_over():
            return False
        
        self.saucer_elapsed += 1
        factor = 800 - self.saucer_elapsed
        factor += randint(0, len(self.asteroids) * 5)
        factor -= randint(0, self.stats.level * 50)
        if factor < 0:
            self.saucer_elapsed = 0
            
        return factor < 0
    
    # Start a new game
    def new_game(self):
        
        self.stars = []
        sec = Dimension(ScreenSize.width / 8, ScreenSize.height / 5)
        for x in xrange(8):
            for y in xrange(5):
                bounds = Rectangle(x * sec.width, y * sec.height, sec.width, sec.height)
                self.stars.append(Star(bounds))
        
        self.stats = Statistics()
        self.asteroids = []
        self.saucers = []
        self.bullets = []
        self.ship = Ship()
        self.saucer_elapsed = 0
        self.next_level()

    # Start the next level
    def next_level(self):
        self.stats.level += 1
        for i in xrange(self.stats.level + 2):
            self.asteroids.append(Asteroid())
        self.mixer.music.play()

    # Return if the level is complete
    def level_complete(self):
        return len(self.asteroids) == 0 and len(self.saucers) == 0
    
    # Return if the game is over
    def game_over(self):
        return self.stats.ships == 0
    
class Statistics(object):
    
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
    def earned_life(self):
        return (self.score - (self.extras * 10000)) > 10000
