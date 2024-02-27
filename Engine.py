from wadData import WadData
from init import *
from ScreenHandler import ScreenHandler
from Player import Player
from Bsp import BSP
from enum import Enum



class _3DEngine:

    def __init__(self, wad_path='data/DOOM.WAD'):
        self.screen = pygame.display.set_mode(SIZE, pygame.DOUBLEBUF)
        pygame.mouse.set_visible(False)
        pygame.mouse.set_pos(WIDTH / 2, HEIGHT / 2)
        self.SW2, self.SH2 = self.screen.get_rect().center
        self.clock = pygame.time.Clock()
        self.running = True

        self.wad_path = wad_path
        self.wad_data = WadData(self, map_name='E1M1')

        self.screenHdlr = ScreenHandler(self)
        self.screenHdlr.set_normals(50, WIDTH - 50, 50, HEIGHT - 50)
        self.Player = Player(self)
        self.Bsp = BSP(self)
        
        

    def mainLoop(self):
        while self.running:
            self.checkEvents()
            self.update()
            self.clock.tick(FRAMERATE)


    def checkEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or\
                (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                self.running = False

    def update(self):
        self.screen.fill('black')
        self.Player.update()
        self.draw()
        
        
        
        

    def get_linedef_sidedefs(self, linedef: Linedef):
        front_sidedef = self.wad_data.sidedefs[linedef.Front_Sidedef]
        back_sidedef = self.wad_data.sidedefs[linedef.Back_Sidedef] if linedef.Back_Sidedef != 0xFFFF else None
        return front_sidedef, back_sidedef
    
    def get_sidedef_sector(self, sidedef: Sidedef):
        return self.wad_data.sectors[sidedef.Sector_id]
    
    def get_seg_sidedefs(self, seg: Seg):
        linedef = self.get_seg_linedef(seg)
        front, back =  self.get_linedef_sidedefs(linedef)
        if seg.Direction:
            front, back = back, front
        return front, back
    
    def get_seg_vertecies(self, seg: Seg):
        start_vertex = self.wad_data.vertecies[seg.Vertex_start]
        end_vertex = self.wad_data.vertecies[seg.Vertex_end]
        return start_vertex, end_vertex
    
    def get_seg_linedef(self, seg: Seg):
        return self.wad_data.linedefs[seg.Linedef_id]
    
        


    def check_bbox(self, bbox):
        a = Vertex(bbox.l, bbox.b)
        b = Vertex(bbox.l, bbox.t)
        c = Vertex(bbox.r, bbox.t)
        d = Vertex(bbox.r, bbox.b)
        facing_side = None
        x, y = self.Player.pos
        # положение игрока от bbox
        TOP = y > bbox.t
        BOTTOM = y < bbox.b
        LEFT = x < bbox.l
        RIGHT = x > bbox.r
        MIDDLE_X = bbox.l < x < bbox.r
        MIDDLE_Y = bbox.b < y < bbox.t
        if TOP and LEFT:
            facing_side = (b, a), (c, b)
        
        elif TOP and MIDDLE_X:
            facing_side = (c, b),
        
        elif TOP and RIGHT:
            facing_side = (c, b), (d, c)
        
        elif MIDDLE_Y and LEFT:
            facing_side = (b, a),
        
        elif MIDDLE_Y and RIGHT:
            facing_side = (d, c),
        
        elif BOTTOM and LEFT:
            facing_side = (b, a), (a, d)
        
        elif BOTTOM and MIDDLE_X:
            facing_side = (a, d), 
        
        elif BOTTOM and RIGHT:
            facing_side = (a, d), (d, c)
        else:
            return True
        # else : player inside of bbox which is excluded in Bsp().render_Bsp()
        for v1, v2 in facing_side:
            a1 = self.angle_to_vertex(v1)
            a2 = self.angle_to_vertex(v2)
            span = self.norm(a1 - a2)
            a1 -= self.Player.angle # make player angle eq to 0
            span1 = self.norm(a1 + H_FOV) # condition for first ray
            if span1 >= span + FOV:
                continue
            return True
        return False

    def angle_to_vertex(self, vertex: Vertex):
        dx, dy = vertex - self.Player.pos
        return self.norm(math.degrees(math.atan2(dy, dx)))
    
    def angle_to_x(self, angle):
        return int(SCREEN_DIST - math.tan(math.radians(angle)) * (WIDTH / 2))
        

    def seg_in_fov(self, v1, v2):
        a1 = self.angle_to_vertex(v1)
        a3 = a1 # nado dlya SH.handle_seg(), save angle to first vertex
        a2 = self.angle_to_vertex(v2)
        span = self.norm(a1 - a2)
        if span >= 180:
            return False
        
        a1 -= self.Player.angle
        a2 -= self.Player.angle
        span1 = self.norm(a1 + H_FOV)
        span2 = self.norm(H_FOV - a2)
        if span1 > FOV:
            if span1 >= span + FOV:
                return False
            a1 = H_FOV
        if span2 > FOV:
            if span1 >= span + FOV:
                return False
            a2 = -H_FOV
        
        x1 = self.angle_to_x(a1)
        x2 = self.angle_to_x(a2)
        return x1, x2, a3
    
    def classify_segment(self, seg: Seg, x1, x2, angle_to_v1):
        segment_class = None
        if x1 == x2:
            return
        front_sidedef, back_sidedef = self.get_seg_sidedefs(seg)
        if not back_sidedef:
        
            segment_class = SEG_CLASSES.WALL
        
        return segment_class

        
    

    
    def norm(self, angle): # norms angle to 0 -> 360
        angle %= 360
        return angle + 360 if angle < 0 else angle


    def draw(self):
       self.screenHdlr.draw()
       pygame.display.flip()



if __name__ == "__main__":
    Engine = _3DEngine()
    Engine.mainLoop()