from init import *


class BSP:
    def __init__(self, engine):
        self.Engine = engine
        self.Player = engine.Player
        self.vertecies = engine.wad_data.vertecies
        self.nodes = engine.wad_data.nodes
        self.segs = engine.wad_data.segs
        self.ssectors = engine.wad_data.ssectors
        self.root_node = len(self.nodes) - 1
        self.traverse_further = True
    
    def update(self):
        self.traverse_further = True
        self.render_Bsp(self.root_node)
    
    
    def render_Bsp(self, node_id):
        if not self.traverse_further:
            return
        
        if node_id >= SSECTOR_ID:
            ssector_id = node_id - SSECTOR_ID
            self.render_ssector(ssector_id)
            return 

        node = self.nodes[node_id]
        on_right = self.player_on_right_side(node)
        if on_right:
            self.render_Bsp(node.Child_r)
            if self.Engine.check_bbox(node.Bbox_l):
                self.render_Bsp(node.Child_l)
        else:
            self.render_Bsp(node.Child_l)
            if self.Engine.check_bbox(node.Bbox_r):
                self.render_Bsp(node.Child_r)
    
    def render_ssector(self, ssector_id):    
        ssector = self.ssectors[ssector_id]
        for i in range(ssector.Seg_count):
            if not self.traverse_further:
                return
            seg = self.segs[ssector.First_seg_id + i]
            cords = self.Engine.seg_in_fov(self.vertecies[seg.Vertex_start], self.vertecies[seg.Vertex_end])
            if cords:
                self.Engine.screenHdlr.handle_seg(seg, *cords)


    def player_on_right_side(self, node): # right side of bst is front and left side is back 
        # результат векторного произведения - ортогональный вектор, поэтому
        # векторное произведение позволяет узнать величину угла между ними,
        # а значит и взаимное расположние
        # векторное произведение > 0 значит вектор направлен вверх, значит игрок находится справа
        
        playerX, playerY = self.Player.pos
        partitionX, partitionY = node.Partition_start
        playerV = Vertex(playerX - partitionX, playerY - partitionY)
        partitionV = Vertex(node.dx, node.dy)
        return playerV.cross(partitionV) > 0 
