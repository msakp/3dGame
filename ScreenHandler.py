from pygame.draw import *
from init import *


class ScreenHandler:
    def __init__(self, Engine):
        self.Engine = Engine
        self.screen = self.Engine.screen
        self.l = 0
        self.r = WIDTH
        self.t = 0
        self.b = HEIGHT

        sorted_byX = sorted(self.Engine.wad_data.vertecies, key=lambda v: v.x)
        self.maxX, self.minX = sorted_byX[-1].x, sorted_byX[0].x

        sorted_byY = sorted(self.Engine.wad_data.vertecies, key=lambda v: v.y)
        self.maxY, self.minY = sorted_byY[-1].y, sorted_byX[0].y

        self.vertecies = [self.normalize(vertex) for vertex in self.Engine.wad_data.vertecies]
        self.linedefs = self.Engine.wad_data.linedefs

        self.handled_seg = None # current segment in handling
        self.a_to_seg_v1 = None

        # screen coords to angle table
        self.px_to_angle = [math.degrees(math.atan((WIDTH // 2 - i) / SCREEN_DIST)) for i in range(0, WIDTH + 1)] 
        # for walls clipping
        self.init_free_space()
    
    def init_free_space(self):
        self.free_space = set(range(WIDTH))

    def set_normals(self, l, r, t, b):
        self.l = l
        self.r = r
        self.t = t
        self.b = b
        self.vertecies = [self.normalize(vertex) for vertex in self.Engine.wad_data.vertecies]
    
    def normalize(self, V: Vertex):
        l, r, t, b = self.l, self.r, self.t, self.b
        minX, maxX, minY, maxY = self.minX, self.maxX, self.minY, self.maxY
        
        
        x, y = V
        # normalized* x and y coordinates by l r t b params
        # with origin of left-top corner
        nx = (x - minX) * (r - l) / (maxX - minX) + l
        ny = HEIGHT - (y - minY) * (b - t) / (maxY - minY) - t
        
        return Vertex(nx, ny / ASPECT)
    
    def get_y_scale(self, x,  ort_dist_to_seg):
        a_of_x = self.px_to_angle[x]
        D = SCREEN_DIST * math.cos(math.radians(self.handled_seg.Angle + 90 - self.Engine.Player.angle - a_of_x))
        d = ort_dist_to_seg * math.cos(math.radians(a_of_x))
        
        return min(MAX_SCALE, max(D / d, MIN_SCALE)) # scale limited by MAX_ / MIN_SCALE (init.py)
        
    def draw_wall(self, x1, x2):
        front_sidedef, _ = self.Engine.get_seg_sidedefs(self.handled_seg)
        front_sector = self.Engine.get_sidedef_sector(front_sidedef)
        
        wall_texture = front_sidedef.Middle_texture
        ceil_texture = front_sector.Ceil_texture
        floor_texture = front_sector.Floor_texture
        light_level = front_sector.Light_level

        ceil_z = front_sector.Ceil_height - self.Engine.Player.height
        floor_z = front_sector.Floor_height - self.Engine.Player.height

        a = self.handled_seg.Angle + 90 - self.a_to_seg_v1
        ort_dist_to_seg = math.cos(math.radians(a)) * math.dist(self.Engine.Player.pos, self.Engine.get_seg_vertecies(self.handled_seg)[0])
        
        scale1 = self.get_y_scale(x1, ort_dist_to_seg)
        if x1 < x2:
            scale2 = self.get_y_scale(x2, ort_dist_to_seg)
            linear_step = (scale2 - scale1) / (x2 - x1) # linear interpolation step
        else:
            linear_step = 0
        y1 = (HEIGHT // 2 + self.Engine.Player.Y_angle) - ceil_z * scale1
        y1_step = -linear_step * ceil_z

        y2 = (HEIGHT // 2 + self.Engine.Player.Y_angle) - floor_z * scale1
        y2_step = -linear_step * floor_z

        for x in range(x1, x2 + 1):
            if ceil_z > 0: # drawing ceiling
                pass
            if floor_z < 0: # drawing floor
                pass
            if wall_texture != '-': # drawing wall
                gfx.vline(self.screen, x, int(y1 - 1), int(y2), (255, 255, 255))

            y1 += y1_step
            y2 += y2_step
       
    def clip_wall(self, x1, x2):
        if self.free_space:
            wall_space = set(range(x1, x2))
            intersection = self.free_space & wall_space
        
            if intersection and len(intersection) == len(wall_space):
                self.draw_wall(x1, x2 - 1)

            elif intersection:
                ordered_intersected_space = sorted(intersection)
                x_s, x_2 = ordered_intersected_space[0], ordered_intersected_space[-1]
                for x_1, x_2 in zip(ordered_intersected_space, ordered_intersected_space[1:]):
                    if x_2 - x_1 > 1: 
                        self.draw_wall(x_s, x_1)
                        x_s = x_2
                self.draw_wall(x_s, x_2)
            
            self.free_space -= intersection
        
        else:
            self.Engine.Bsp.travesre_further = False
            

        


    def handle_seg(self, seg: Seg, x1, x2, angle_to_v1):
        self.a_to_seg_v1 = angle_to_v1
        self.handled_seg = seg
        _class = self.Engine.classify_segment(seg, x1, x2, angle_to_v1)
        if _class == SEG_CLASSES.WALL:
            self.clip_wall(x1, x2)
        
    
    def draw(self):
        self.init_free_space()
        self.Engine.Bsp.update()
