# Author: Jonathan Jengo

import os
import pygame
from .asteroid import Asteroid
from .saucer import Saucer

# Various sounds
SmallBang, MediumBang, LargeBang, Extra, Fire, LargeSaucer, SmallSaucer, Thrust, Music = range(9)

# Load a sound from the file system
def load(filename):
    return pygame.mixer.Sound(os.path.join("sounds", filename))

# Sound mixer
class Mixer:
    
    # Initialize
    def __init__(self):
        self.sounds = {}
        self.sounds[SmallBang] = load("bangSmall.wav")
        self.sounds[MediumBang] = load("bangMedium.wav")
        self.sounds[LargeBang] = load("bangLarge.wav")
        self.sounds[Extra] = load("extraShip.wav")
        self.sounds[Fire] = load("fire.wav")
        self.sounds[LargeSaucer] = load("saucerBig.wav")
        self.sounds[SmallSaucer] = load("saucerSmall.wav")
        self.sounds[Thrust] = load("thrust.wav")
        self.sounds[Music] = Music()
        self.looping = {}

    # Play a sound
    def play(self, key, loops = 0):
        if loops == -1:
            self.loop(key)
        else:
            self.sounds[key].play(loops)
            
    # Play a looping sound
    def loop(self, key):
        if not key in self.looping or not self.looping[key]:
            self.sounds[key].play(-1)
            self.looping[key] = True

    # Stop playing a sound
    def stop(self, key):
        self.sounds[key].stop()
        if key in self.looping:
            self.looping[key] = False
                        
    # Def update any custom sounds
    def update(self):
        self.sounds[Music].update()
            
    # Pause all playback of sounds
    def pause(self):
        pygame.mixer.pause()
        
    # Resume all playback of sounds
    def unpause(self):
        pygame.mixer.unpause()
            
    # Stop playback of all sounds
    def stopall(self):
        self.sounds[Music].stop()
        for key in self.looping:
            self.sounds[key].stop()
            self.looping[key] = False
        
    # Play bang sound for asteroid
    def playAsteroidBang(self, asteroid):
        if asteroid.size == Asteroid.Large:
            self.play(LargeBang)
        elif asteroid.size == Asteroid.Medium:
            self.play(MediumBang)
        else:
            self.play(SmallBang)
    
    # Play bang sound for saucer
    def playSaucerBang(self, saucer):
        if saucer.size == Saucer.Large:
            self.play(MediumBang)
        else:
            self.play(SmallBang)
        
    # Loop sound for live saucer
    def loopLiveSaucer(self, saucer):
        if saucer.size == Saucer.Large:
            self.loop(LargeSaucer)
        else:
            self.loop(SmallSaucer)

    # Stop sound for saucer
    def stopLiveSaucer(self, saucer):
        if saucer.size == Saucer.Large:
            self.stop(LargeSaucer)
        else:
            self.stop(SmallSaucer)
        
# Background music
class Music:
    
    FlipStart = 35.0
    FlipMin = 9.0
    BeatDecay = 0.4
    
    # Initialize
    def __init__(self):
        self.beats = []
        self.beats.append(load("beat1.wav"))
        self.beats.append(load("beat2.wav"))
        self.curr = 0
        self.flipTime = self.FlipStart
        self.timeToFlip = 2
        self.playing = False
        
    # Loop music in alternating tones
    def play(self, loops):
        if not self.playing:
            self.flipTime = self.FlipStart
            self.timeToFlip = 2
            self.playing = True
            
    # Def play current beat
    def playbeat(self):
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
            self.timeToFlip -= 1
            if self.timeToFlip <= 0:
                if (self.flipTime > self.FlipMin):
                    self.flipTime -= self.BeatDecay
                self.timeToFlip = self.flipTime
                self.playbeat()
    