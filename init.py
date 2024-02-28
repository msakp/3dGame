import pygame
import pygame.gfxdraw as gfx
import math
from data_types import *
from numba import jit, njit
from enum import Enum


FRAMERATE = 60
DOOM_RES = DOOM_W, DOOM_H = 320, 200
ASPECT = DOOM_W / DOOM_H # original 16/10 so window will be stretched
SIZE = WIDTH, HEIGHT = 1600, 1000
SCALE = 5
FOV = 90
H_FOV = FOV / 2
SCREEN_DIST = int((WIDTH / 2) / math.tan(math.radians(H_FOV)))

# max and minimul scale factor, (doom textures will act normal, if scale is between )
MAX_SCALE = 64
MIN_SCALE = 0.00390625  

PLAYER_SPEED_PER_TICK = 4
PLAYER_HEIGHT = 45

SSECTOR_ID = 0x8000

class SEG_CLASSES(Enum):
        WALL = 0
        PORTAL = 1

pygame.init()
pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP,
                          pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP])

