import os
import pygame
from asteroids.asteroid import Asteroid
from asteroids.saucer import Saucer

# Load a sound from the file system
def load(filename):
    return pygame.mixer.Sound(os.path.join("sounds", filename))

class Sound(object):
    def __init__(self, filename):
        self.sound = load(filename)
        self.looping = False
    def play(self, loops=0):
        self.sound.play(loops)
    def loop(self):
        if not self.looping:
            self.sound.play(-1)
            self.looping = True
    def stop(self):
        self.sound.stop()
        self.looping = False

class Mixer(object):

    def __init__(self):
        self.small_bang = Sound('bangSmall.wav')
        self.medium_bang = Sound('bangMedium.wav')
        self.large_bang = Sound('bangLarge.wav')
        self.extra = Sound('extraShip.wav')
        self.fire = Sound('fire.wav')
        self.large_saucer = Sound('saucerBig.wav')
        self.small_saucer = Sound('saucerSmall.wav')
        self.thrust = Sound('thrust.wav')
        self.music = Music()

    def update(self):
        self.music.update()
            
    def pause(self):
        pygame.mixer.pause()
        
    def unpause(self):
        pygame.mixer.unpause()
            
    def stopall(self):
        self.small_bang.stop()
        self.medium_bang.stop()
        self.large_bang.stop()
        self.extra.stop()
        self.fire.stop()
        self.large_saucer.stop()
        self.small_saucer.stop()
        self.thrust.stop()
        self.music.stop()
        
    # Play bang sound for asteroid
    def play_asteroid_bang(self, asteroid):
        sounds = {
            Asteroid.Large: self.large_bang,
            Asteroid.Medium: self.medium_bang,
            Asteroid.Small: self.small_bang
        }
        sounds.get(asteroid.size).play()
    
    # Play bang sound for saucer
    def play_saucer_bang(self, saucer):
        sounds = {
            Saucer.Large: self.medium_bang,
            Saucer.Small: self.small_bang
        }
        sounds.get(saucer.size).play()
        
    # Stop sound for saucer
    def stop_live_saucer(self, saucer):
        sounds = {
            Saucer.Large: self.large_saucer,
            Saucer.Small: self.small_saucer
        }
        sounds.get(saucer.size).stop()
        
# Background music
class Music(object):
    
    FlipStart = 35.0
    FlipMin = 9.0
    BeatDecay = 0.4
    
    def __init__(self):
        self.beats = []
        self.beats.append(load("beat1.wav"))
        self.beats.append(load("beat2.wav"))
        self.curr = 0
        self.flip_time = self.FlipStart
        self.time_to_flip = 2
        self.playing = False
        
    # Loop music in alternating tones
    def play(self):
        if not self.playing:
            self.flip_time = self.FlipStart
            self.time_to_flip = 2
            self.playing = True
            
    # Def play current beat
    def play_beat(self):
        self.beats[self.curr].play(0)
        self.curr += 1
        if self.curr > 1:
            self.curr = 0
    
    # Stop music.
    def stop(self):
        self.playing = False
        
    # Update music beat
    def update(self):
        if self.playing:
            self.time_to_flip -= 1
            if self.time_to_flip <= 0:
                if self.flip_time > self.FlipMin:
                    self.flip_time -= self.BeatDecay
                self.time_to_flip = self.flip_time
                self.play_beat()
    