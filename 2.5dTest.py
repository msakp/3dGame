import pygame
import os
import math
import time
from Tools import *
from Sprites import *
from MatrixClasses import *


pygame.init()
pygame.display.set_caption('arcade *2.5d*')

WIDTH, HEIGHT = size = 1920, 1080

screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
clock = pygame.time.Clock()
FPS = 60

#==============Groups=============#
all_sprites = pygame.sprite.Group()
minimap_group = pygame.sprite.GroupSingle()

#===============Setup=============#

layout = load_level('test.txt')


minimap = MiniMap(minimap_group, layout)
meter = Meter(all_sprites)
matrix = Matrix(screen, WIDTH, HEIGHT)


center_pos = (WIDTH / 2, HEIGHT / 2) # default mouse pos
pygame.mouse.set_visible(False)
pygame.event.set_grab(True)  # lock the mouse
playerX, playerY = minimap.getPlayer()
playerA = 0
YAngle = 0
FOV = 3.14159 / 4
speed = 5 # blocks per second !
elapsedTime = 1 / 1000

move_R = False
move_L = False
move_U = False
move_D = False
move_W = False
move_T = False
move = False
mouse_move = False

matrix.render(playerX, playerY, playerA, FOV, layout, YAngle)
minimap_group.draw(screen)
meter.update(playerX, playerY, playerA, YAngle, 60)
        
    

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
        
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
             terminate()


        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                move_U = True
            elif event.key == pygame.K_d:
                move_D = True
            elif event.key == pygame.K_f:
                move_R = True
            elif event.key == pygame.K_s:
                move_L = True
            elif event.key == pygame.K_w:
                move_W = True
            elif event.key == pygame.K_t:
                move_T = True
            move = True
            

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_e:
                move_U = False
            elif event.key == pygame.K_d:
                move_D = False
            elif event.key == pygame.K_f:
                move_R = False
            elif event.key == pygame.K_s:
                move_L = False
            elif event.key == pygame.K_w:
                move_W = False
            elif event.key == pygame.K_t:
                move_T = False
            pressed = tuple(filter(lambda key: key, pygame.key.get_pressed()))
            if not pressed:
                move = False
        
        elif event.type == pygame.MOUSEMOTION:
            dx = event.rel[0] / 1000
            dy = event.rel[1] / 2

            pygame.mouse.set_pos(screen.get_rect().center)
            playerA += dx
            YAngle -= dy
            if YAngle > 300 or YAngle < -200:
                YAngle += dy
            mouse_move = True
        
        elif event.type == pygame.MOUSEWHEEL:
            FOV += event.y * 0.05

    

    #==============MOVE UPDATE================#
    frameSpeed = speed * elapsedTime
    if move_U:
        playerX += math.sin(playerA) * frameSpeed
        playerY += math.cos(playerA) * frameSpeed
        if layout[int(playerY)][int(playerX)] == '#':
                playerX -= math.sin(playerA) * frameSpeed
                playerY -= math.cos(playerA) * frameSpeed
        

    if move_D:
        playerX -= math.sin(playerA) * frameSpeed
        playerY -= math.cos(playerA) * frameSpeed
        if layout[int(playerY)][int(playerX)] == '#':
            playerX += math.sin(playerA) * frameSpeed
            playerY += math.cos(playerA) * frameSpeed
            

        
    if move_R:
            playerX += 0.75 * math.cos(playerA) * frameSpeed
            playerY -= 0.75 * math.sin(playerA) * frameSpeed

            if layout[int(playerY)][int(playerX)] == '#':
                playerX -= 0.75 * math.cos(playerA) * frameSpeed
                playerY += 0.75 * math.sin(playerA) * frameSpeed
    if move_L:
            playerX -= 0.75 *  math.cos(playerA) * frameSpeed
            playerY += 0.75 * math.sin(playerA) * frameSpeed
            if layout[int(playerY)][int(playerX)] == '#':
                playerX += 0.75 * math.cos(playerA) * frameSpeed
                playerY -= 0.75 * math.sin(playerA) * frameSpeed
    
    if move or mouse_move:
        screen.fill('black')
        minimap.update(int(playerX), int(playerY))
        matrix.render(playerX, playerY, playerA, FOV, layout, YAngle)
        minimap_group.draw(screen)
        mouse_move = False

    #=========================================#
    all_sprites.draw(screen)
    pygame.display.flip()
    elapsedTime = clock.tick() / 1000
    fps = 0 if not elapsedTime else int(60 / elapsedTime / 100)
    meter.update(playerX, playerY, playerA, YAngle, fps)
    
    #clock.tick(FPS)
    
