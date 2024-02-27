from init import *
class Player:
    def __init__(self, engine):
        self.Engine = engine
        self.thing = engine.wad_data.things[0]
        self.pos = self.thing.Pos
        self.angle = self.thing.Angle
        self.Y_angle = 0
        self.height = PLAYER_HEIGHT
    

    def update(self):
        dx, dy = pygame.mouse.get_rel()
        x, y = pygame.mouse.get_pos()
        pygame.mouse.set_pos(x - dx, y - dy)
        self.angle = self.Engine.norm(self.angle - dx / 4)
        self.Y_angle -= dy * 1.2


        inc = Vertex(0, 0)
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_e]:
            inc += Vertex(PLAYER_SPEED_PER_TICK, 0).rotate(self.angle)
        if keys_pressed[pygame.K_d]:
            inc -= Vertex(PLAYER_SPEED_PER_TICK, 0).rotate(self.angle)
        if keys_pressed[pygame.K_f]:
            inc -= Vertex(0, PLAYER_SPEED_PER_TICK).rotate(self.angle)
        if keys_pressed[pygame.K_s]:
            inc += Vertex(0, PLAYER_SPEED_PER_TICK).rotate(self.angle)
        if inc.x and inc.y:
            inc /= (2 ** 0.5)

        self.pos += inc

        
        
