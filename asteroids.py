# Author: Jonathan Jengo

import os
import sys
import pygame
from asteroids.core import Core
from asteroids.util import ScreenSize

# Initialize
os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.mixer.pre_init(44100, -16, 2, 4096)
pygame.init()
gfx = pygame.display.set_mode(ScreenSize)
pygame.display.set_caption('Asteroids')

# Start asteroids game
if __name__ == '__main__':
    Core(gfx).run()