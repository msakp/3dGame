import pygame
import os
import math
import time
from Tools import *
from Sprites import *
from MatrixClasses import *


pygame.init()
pygame.display.set_caption('arcade *2.5d*')
WIDTH, HEIGHT = size = 800, 450
screen = pygame.display.set_mode(size, pygame.SCALED)
clock = pygame.time.Clock()
FPS = 30

#==============Groups=============#
all_sprites = pygame.sprite.Group()
minimap_group = pygame.sprite.GroupSingle()

#===============Setup=============#

layout = load_level('map.txt')

minimap = MiniMap(minimap_group, layout)
meter = Meter(all_sprites)
matrix = Matrix(screen, WIDTH, HEIGHT)


playerX, playerY = 1.5, 1
playerA = 0
YAngle = 0
FOV = 3.14159 / 4
speed = 1 / 12 # blocks per frame !

move_U = False
move_D = False
move_R = False
move_L = False

matrix.render(playerX, playerY, playerA, FOV, layout, YAngle)
minimap_group.draw(screen)
meter.update(playerX, playerY, playerA, YAngle)
pygame.display.flip()
time.sleep(0.5)


def moveUpdate():
    global playerX, playerY, playerA, FOV, layout, YAngle
    dx = math.sin(playerA) * speed
    dy = math.cos(playerA) * speed
    playerX += dx
    playerY += dy
    if layout[int(playerY + 0.06)][int(playerX + 0.06)] == '#' or\
     layout[int(playerY - 0.06)][int(playerX - 0.06)] == '#':
            terminate()
    if move_R:
            playerX +=  0.25  * speed
    elif move_L:
            playerX -= 0.25 * speed
    elif move_U:
          YAngle += 1
    elif move_D:
          YAngle -= 1
    
    screen.fill('black')
    minimap.update(int(playerX), int(playerY))
    meter.update(playerX, playerY, playerA, YAngle)
    matrix.render(playerX, playerY, playerA, FOV, layout, YAngle)
    minimap_group.draw(screen)
    
        
    

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                  move_U = True
            if event.key == pygame.K_d:
                  move_D = True
            if event.key == pygame.K_f:
                    move_R = True
            elif event.key == pygame.K_s:
                    move_L = True
            
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_e:
                  move_U = False
            if event.key == pygame.K_d:
                  move_D = False
            if event.key == pygame.K_f:
                    move_R = False
            elif event.key == pygame.K_s:
                    move_L = False
    moveUpdate()
    all_sprites.draw(screen)
    pygame.display.flip()
    clock.tick(FPS)
