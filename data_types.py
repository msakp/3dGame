from pygame import Vector2



class Vertex(Vector2):
    def __init__(self, x, y):
        super().__init__(int(x), int(y)) # always integers

#Типы данных, согласно doomwiki.org

class Linedef:
    __slots__ = [
        "Start_Vertex",
        "End_Vertex",
        "Flags",
        "Special_type",
        "Sector_Tag",
        "Front_Sidedef",
        "Back_Sidedef"
    ]
    def __init__(self, start, end, flags, type, tag, front, back):
        self.Start_Vertex = start
        self.End_Vertex = end
        self.Flags = flags
        self.Special_type = type
        self.Sector_Tag = tag
        self.Front_Sidedef = front
        self.Back_Sidedef = back

class Sidedef:
    __slots__ = [
        "Offset", # (x, y) # int16_t, 4bytes
        "Upper_texture", # char 8bytes
        "Lower_texture", # char 8bytes
        "Middle_texture", # char 8bytes
        "Sector_id", # uint16_t 2bytes
    ]
    def __init__(self, offset, upper_t, lower_t, middle_t, ssector_id):
        self.Offset = offset
        self.Upper_texture = upper_t
        self.Lower_texture = lower_t
        self.Middle_texture = middle_t
        self.Sector_id = ssector_id

class Bbox:
        __slots__ = ['t', 'b', 'l', 'r']

class Node:

    __slots__ = [
        "Partition_start", # int16_t, 2bytes
        "dx", # int16_t, 2bytes
        "dy", # int16_t, 2bytes
        "Bbox_r", # int16_t[4], 8bytes
        "Bbox_l", # int16_t[4], 8bytes
        "Child_r", # uint16_t, 2bytes
        "Child_l" # uint16_t, 2bytes
    ]

    def __init__(self, start, dx, dy, Bbox_r, Bbox_l, Child_r, Child_l):
        self.Partition_start = start
        self.dx = dx
        self.dy = dy
        self.Bbox_r = Bbox_r
        self.Bbox_l = Bbox_l
        self.Child_r = Child_r
        self.Child_l = Child_l


class Sector:
    __slots__ = [
        "Floor_height", # int16_t, 2bytes
        "Ceil_height", # int16_t, 2bytes
        "Floor_texture", # char 8bytes
        "Ceil_texture", # char 8bytes 
        "Light_level", # uint16_t, 2bytes
        "Type", # uint16_t, 2bytes
        "Tag" # uint16_t, 2bytes
    ]
    def __init__(self, floor_h, ceil_h, floor_t, ceil_t, light_level, type, tag):
        self.Floor_height = floor_h
        self.Ceil_height = ceil_h
        self.Floor_texture = floor_t
        self.Ceil_texture = ceil_t
        self.Light_level = light_level
        self.Type = type
        self.Tag = tag

class Seg:
    __slots__ = [
        "Vertex_start", #int16_t, 2bytes
        "Vertex_end", #int16_t, 2bytes
        "Angle", #int16_t, 2bytes
        "Linedef_id", #int16_t, 2bytes
        "Direction", # 0(same as linedef) / 1(opposite of linedef) int16_t, 2bytes
        "Offset", #int16_t, 2bytes
    ]
    def __init__(self, start, end, angle, linedef, direction, offset):
        self.Vertex_start = start
        self.Vertex_end = end
        angle = (angle << 16) * 8.381903117e-8 # converting angle from BAM to degree
        self.Angle = angle + 360 if angle < 0 else angle
        self.Linedef_id = linedef
        self.Direction = direction
        self.Offset = offset

class SSector:
    __slots__ = [
        "Seg_count", # int16_t, 2bytes
        "First_seg_id" # int16_t, 2bytes
    ]
    def __init__(self, seg_count, first_seg):
        self.Seg_count = seg_count
        self.First_seg_id = first_seg

class Thing:
    __slots__ = [
        "Pos", # int16_t, 2bytes
        "Angle", # uint16_t, 2bytes
        "Type", # uint16_t, 2bytes
        "Flags" # uint16_t, 2bytes
    ]
    def __init__(self, pos, angle, type, flags):
        self.Pos = pos
        self.Angle = angle
        self.Type = type
        self.Flags = flags
