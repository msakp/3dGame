import numpy as np
from math import *
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *


WIDTH, HEIGHT = size = 800, 600
scale = 100
Angle = 0

screen = pygame.display.set_mode(size, DOUBLEBUF|OPENGL)
glViewport(0, 0, WIDTH, HEIGHT);
glMatrixMode(GL_PROJECTION);
glLoadIdentity();
glOrtho(0, WIDTH, HEIGHT, 0, -1, 1);
glMatrixMode(GL_MODELVIEW);
glLoadIdentity();

clock = pygame.time.Clock()

points = []

points.append(np.matrix([-1, -1, 1]))
points.append(np.matrix([1, -1, 1]))
points.append(np.matrix([1, 1, 1]))
points.append(np.matrix([-1, 1, 1]))
points.append(np.matrix([-1, -1, -1]))
points.append(np.matrix([1, -1, -1]))
points.append(np.matrix([1, 1, -1]))
points.append(np.matrix([-1, 1, -1]))
points = [point.reshape(3, 1) for point in points]

projection_matrix = np.matrix([
    [1, 0, 0],
    [0, 1, 0],
    
])

rotationX_matrix = np.matrix([
    [1, 0, 0],
    [0, cos(Angle), -sin(Angle)],
    [0, sin(Angle), cos(Angle)]
])


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False
        

    rotationX_matrix = np.matrix([
    [1, 0, 0],
    [0, cos(Angle), -sin(Angle)],
    [0, sin(Angle), cos(Angle)]
    ])
    rotationZ_matrix = np.matrix([
    [cos(Angle), -sin(Angle), 0],
    [sin(Angle), cos(Angle), 0],
    [0, 0, 1]
    ])
    rotationY_matrix = np.matrix([
        [cos(Angle), 0, sin(Angle)],
        [0, 1, 0],
        [-sin(Angle), 0, cos(Angle)]
    ])
    for point in points:
        rotated = np.dot(rotationY_matrix, point)
        projection = np.dot(projection_matrix, rotated)
        x = int(projection[0][0] * scale) + WIDTH / 2
        y = int(projection[1][0] * scale) + HEIGHT / 2
        
        glColor3f(255, 255, 255)
        glPointSize(4)
        glBegin(GL_POINTS)
        glVertex2f(x, y)
        glEnd()

    pygame.display.flip()
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    clock.tick(120)
    Angle += 0.01