import pygame
import math

class Matrix:
    def __init__(self, screen, screenW, screenH):
        self.cell_size = 2
        self.screen = screen
        self.res = (int(screenW / self.cell_size), int(screenH / self.cell_size))

    def render(self, playerX, playerY, playerA, FOV, layout, YAngle):
        YAngle = int(YAngle)
        CeilingRect = None
        FloorRect = None
        WallRect = None
        prevC = None
        Color = '#8a8a8a'
        for x in range(self.res[0]):
            rayAngle = (x / self.res[0]) * FOV + (playerA - FOV / 2)
            step = 0.1
            DistanceToWall = 0
            Depth = 12
            Horizon = self.res[1] / 2
            HitWall = False
            EyeX = math.sin(rayAngle)
            EyeY = math.cos(rayAngle)
            while (not HitWall and DistanceToWall < Depth):
                DistanceToWall += step
                testX = int(playerX + EyeX * DistanceToWall)
                testY = int(playerY + EyeY * DistanceToWall)
                if testX < 0 or testY < 0 or testX >= len(layout[0]) or testY >= len(layout):
                    HitWall = True
                    DistanceToWall = Depth
                elif layout[testY][testX] == '#':
                    HitWall = True

            DistanceToWall *= math.cos(playerA - rayAngle)
            Ceiling = int(Horizon - self.res[1] / DistanceToWall)
            Floor = self.res[1] - Ceiling + YAngle
            Ceiling += YAngle
            """if DistanceToWall < Depth / 3:
                Color = '#dadada'
            elif DistanceToWall < Depth / 2:
                Color = '#8a8a8a'
            elif DistanceToWall < Depth / 1.5:
                Color = '#4a4a4a'
            elif DistanceToWall < Depth:
                Color = '#3a3a3a'
            else:
                Color = '#000000'"""
            
            realX = x * self.cell_size
            realC = Ceiling * self.cell_size
            realF = Floor * self.cell_size
            if realC == prevC:
                CeilingRect[2] += self.cell_size
                WallRect[2] += self.cell_size
                FloorRect[2] += self.cell_size
            elif realC != prevC:
                if not x:
                    CeilingRect = [realX, 0, self.cell_size, realC]
                    WallRect = [realX, realC + 1, self.cell_size, realF - realC]
                    FloorRect = [realX, realF, self.cell_size, self.res[1] * self.cell_size]
                pygame.draw.rect(self.screen, '#000000', tuple(CeilingRect))
                pygame.draw.rect(self.screen, Color, tuple(WallRect))
                pygame.draw.rect(self.screen, '#282828', tuple(FloorRect))
                CeilingRect = [realX, 0, self.cell_size, realC]
                WallRect = [realX, realC + 1, self.cell_size, realF - realC]
                FloorRect = [realX, realF, self.cell_size, self.res[1] * self.cell_size]
            prevC = realC
        pygame.draw.rect(self.screen, '#000000', tuple(CeilingRect))
        pygame.draw.rect(self.screen, Color, tuple(WallRect))
        pygame.draw.rect(self.screen, '#282828', tuple(FloorRect))
        '''
                b = 1 - (y - self.res[1] / 2) / (self.res[1] / 2)
                if b < 0.25: Color = '#202020'
                elif b < 0.5: Color = '#222222'
                elif b < 0.75: Color = '#242424'
                elif b < 0.9: Color = '#282828'
                self.matrix[y][x].render(self.screen, Color)'''
            
    
    

