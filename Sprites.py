import pygame

class MiniMap(pygame.sprite.Sprite):
    def __init__(self, group, layout):
        self.cell_size = 8 # in pixels
        self.color = 'grey'
        self.layout = layout
        self.playerCords = None
        super().__init__(group)
        self.image = pygame.Surface((len(layout[0]) * self.cell_size, len(layout) * self.cell_size))
        self.draw_level(self.layout)
        self.rect = self.image.get_rect()
        self.rect.y = 20  
        
        

    def draw_level(self, level):
        for y in range(len(level)):
            for x in range(len(level[y])):
                if level[y][x] == '#':
                    pygame.draw.rect(self.image, self.color, \
                                     (x * self.cell_size , y * self.cell_size,\
                                       x * self.cell_size + self.cell_size, y * self.cell_size + self.cell_size))
                if level[y][x] == '.':
                    pygame.draw.rect(self.image, 'black', \
                                     (x * self.cell_size , y * self.cell_size,\
                                       x * self.cell_size + self.cell_size, y * self.cell_size + self.cell_size))

                if level[y][x] == 'P':
                    self.playerCords = (x, y)
                    pygame.draw.rect(self.image, 'red', \
                                     (x * self.cell_size , y * self.cell_size,\
                                       x * self.cell_size + self.cell_size, y * self.cell_size + self.cell_size))


    def update(self, new_x, new_y):
        self.image.fill('black')
        x, y = self.playerCords
        self.layout[y] = self.layout[y][:x] + '.' + self.layout[y][x + 1:]
        self.layout[new_y] = self.layout[new_y][:new_x] + 'P' + self.layout[new_y][new_x + 1:]
        self.draw_level(self.layout)
    
    def getPlayer(self): return self.playerCords
        
                    

class Meter(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.image = pygame.Surface((300, 20))
        
        self.rect = self.image.get_rect()
    
    def update(self, x, y, a, ya, fps):
        self.image.fill('black')
        font = pygame.font.Font(None, 20)
        message = f'X: {x:.2f} Y: {y:.2f} A: {a:.2f} YA: {ya:.2f} FPS: {fps}'
        string = font.render(message, 1, 'white')
        self.image.blit(string, (0, 0))
