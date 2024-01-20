import pygame
import math
import numpy as np
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from Gargabe.Tools import *
from Gargabe.Player import *
from Gargabe.Sprites import *

WIDTH, HEIGHT = SIZE = 800, 450
matrixW, matrixH = 200, 112
W2 = WIDTH / 2
H2 = HEIGHT / 2
pixelScale = int(WIDTH / matrixW)

l, r, t, b, f, n = 0, 200, 200, 0, -200, 0 


def pixel(x, y, c):
    r, g, b = int(c[1:3], base=16), int(c[3:5], base=16), int(c[5:], base=16)
    glColor3f(r, g, b)
    glPointSize(pixelScale)
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()

def DrawLine(x1, x2, b1, b2):
    db  = b2 - b1
    dx = x2 - x1 if x2 -x1 else 0
    for x in range(x1, x2):
        y1 = db * (x - x1 + 0.5) / dx + b1
        pixel(x, y1, "#ffffff")

def DrawWall():
   coords = [np.array([0, -20, 0]), np.array([[10, -20, 0]])]
   for vertex in coords: 
        vertex = vertex.reshape(3, 1)
        View = map(lambda v: v[0], vertex)
        Xv, Yv, Zv = View
        
        

    

#=========Init================#    

pygame.init()
screen = pygame.display.set_mode(SIZE, DOUBLEBUF|OPENGL)
clock = pygame.time.Clock()
pygame.mouse.set_visible(False)
pygame.event.set_grab(True)  # lock the mouse

# opengl coordinates origin to left-top
glViewport(0, 0, WIDTH, HEIGHT);
glMatrixMode(GL_PROJECTION);
glLoadIdentity();
glOrtho(0, WIDTH, HEIGHT, 0, -1, 1);
glMatrixMode(GL_MODELVIEW);
glLoadIdentity();


#Init player
PLAYER = Player(0, 0, 0)
SPEED = 5 # pixels per second   
elapsedTime = 0
move_U = False
move_D = False
move_R = False
move_L = False
move_F = False
move_B = False
move_W = False
move_T = False
move = False
mouse_move = False
#=========Game_Loop==========#

DrawWall()
pygame.display.flip()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
            quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                terminate()
                quit()
            elif event.key == pygame.K_e:
                move_F = True
            elif event.key == pygame.K_d:
                move_B = True
            elif event.key == pygame.K_f:
                move_R = True
            elif event.key == pygame.K_s:
                move_L = True
            elif event.key == pygame.K_w:
                move_U = True
            elif event.key == pygame.K_r:
                move_D = True

            move = True
            
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_e:
                move_F = False
            elif event.key == pygame.K_d:
                move_B = False
            elif event.key == pygame.K_f:
                move_R = False
            elif event.key == pygame.K_s:
                move_L = False
            elif event.key == pygame.K_w:
                move_U = False
            elif event.key == pygame.K_r:
                move_D = False
            pressed = tuple(filter(lambda key: key, pygame.key.get_pressed()))
            if not pressed:
                move = False

        elif event.type == pygame.MOUSEMOTION:
            dx, dy = event.rel
            #eeeePLAYER.XAngle += dx / 1000
            PLAYER.YAngle += dy
            pygame.mouse.set_pos(screen.get_rect().center)
            mouse_move = True
        

    #===========MoveUpdate==============#
    speedOfFrame = elapsedTime * SPEED
    dx = 2 * math.sin(PLAYER.XAngle)
    dz = 2 * math.cos(PLAYER.XAngle)
    if move_F:
        PLAYER.x -= dx
        PLAYER.z -= dz

    if move_B:
        PLAYER.x += dx
        PLAYER.z += dz
            
    if move_R:
       PLAYER.x += dy
       PLAYER.z -= dz     

    if move_L:
        PLAYER.x -= dy
        PLAYER.z += dz    
    
    if move_U:
        PLAYER.y += 1

    if move_D:
        PLAYER.y -= 1 
           
    
    if move or mouse_move:
        DrawWall()
        pygame.display.flip()
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        mouse_move = False
        print(PLAYER.getPos())
        
    #===================================#
    #pixel(20, 20, '#ff0000')
    pygame.time.wait(8)
    elapsedTime = (clock.tick() - 8) / 1000
    #clock.tick(120)
    