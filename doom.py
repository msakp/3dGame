import pygame
import math
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from Tools import *
from Player import *
from Sprites import *

WIDTH, HEIGHT = SIZE = 800, 450
matrixW, matrixH = 200, 112
W2 = WIDTH / 2
H2 = HEIGHT / 2
pixelScale = int(WIDTH / matrixW)

def setCord():
    glViewport(0, 0, WIDTH, HEIGHT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0.0, WIDTH, 0.0, HEIGHT)

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
    wx, wy, wz, cos, sin = [], [], [], math.cos(PLAYER.XAngle), math.sin(PLAYER.XAngle)
    x1 = 40 - PLAYER.x
    y1 = 10 - PLAYER.y
    x2 = 40 - PLAYER.x
    y2 = 290 - PLAYER.y
    # world x
    wx.append(x1 * cos - y1 * sin)
    wx.append(x2 * cos - y2 * sin)
    wx.append(wx[0])
    wx.append(wx[1])
    # world depth
    wy.append(y1 * cos + x1 * sin)
    wy.append(y2 * cos + x2 * sin)
    wy.append(wy[0])
    wy.append(wy[1])
    # world height 
    wz.append(0 - PLAYER.z + ((PLAYER.YAngle * wy[0]) / 32))
    wz.append(0 - PLAYER.z + ((PLAYER.YAngle * wy[1]) / 32))
    wz.append(wz[0] + 40)
    wz.append(wz[1] + 40)
    # screen x and y position
    k = 100
    wx[0] = int(wx[0] * k / wy[0] + W2)
    wy[0] = int(-wz[0] * k / wy[0] + H2) 
    wx[1] = int(wx[1] * k / wy[1] + W2)
    wy[1] = int(-wz[1] * k / wy[1] + H2) 

    wx[2] = int(wx[2] * k / wy[2] + W2)
    wy[2] = int(-wz[2] * k / wy[2] + H2) 
    wx[3] = int(wx[3] * k / wy[3] + W2)
    wy[3] = int(-wz[3] * k / wy[3] + H2) 
    

    # draw verticies
    #if wx[0] > 0 and wx[0] < WIDTH and wy[0] > 0 and wy[0] < HEIGHT:
    #    pixel(wx[0], wy[0], '#ffffff')
    #if wx[1] > 0 and wx[1] < WIDTH and wy[1] > 0 and wy[1] < HEIGHT:
    #    pixel(wx[1], wy[1], '#ffffff')
    DrawLine(wx[0], wx[1], wy[0], wy[1])
    DrawLine(wx[2], wx[3], wy[2], wy[3])

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

#Store sin/cos in degrees
for a in range(360):
    MATH.sin.append(math.sin(a / 180 * math.pi))
    MATH.cos.append(math.cos(a / 180 * math.pi))
#Init player
PLAYER = Player(70, -110, 20)
SPEED = 100 # pixels per second   
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
            PLAYER.XAngle += dx / 1000
            PLAYER.YAngle += dy
            pygame.mouse.set_pos(screen.get_rect().center)
            mouse_move = True
        

    #===========MoveUpdate==============#
    speedOfFrame = elapsedTime * SPEED
    dx = 2 * math.sin(PLAYER.XAngle)
    dy = 2 * math.cos(PLAYER.XAngle)
    if move_F:
        PLAYER.x += dx
        PLAYER.y += dy

    if move_B:
        PLAYER.x -= dx
        PLAYER.y -= dy
            
    if move_R:
       PLAYER.x += dy
       PLAYER.y -= dx     

    if move_L:
        PLAYER.x -= dy
        PLAYER.y += dx    
    
    if move_U:
        PLAYER.z += 1

    if move_D:
        PLAYER.z -= 1 
           
    
    if move or mouse_move:
        DrawWall()
        pygame.display.flip()
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        mouse_move = False
        
    #===================================#
    #pixel(20, 20, '#ff0000')
    pygame.time.wait(8)
    elapsedTime = (clock.tick() - 8) / 1000
    #clock.tick(120)
    