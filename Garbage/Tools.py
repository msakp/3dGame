import  sys, pygame
from enum import Enum
from dataclasses import dataclass

def terminate():
    pygame.quit()
    sys.exit()


def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    return level_map


class trackMap(Enum):
    LINE = 0
    TILTR = 1
    TILTL = 2
    TURNR = 3
    TURNL = 4



def map_generator(name, *track_parts): # such as: (LINE, number);(TILTR, bool);(TILTL;bool);()
    for part in track_parts:
        pass

@dataclass
class Functions:
    sin = []
    cos = []

MATH = Functions()
