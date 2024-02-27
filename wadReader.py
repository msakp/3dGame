import struct
from init import *

class WadReader:
    # for struct.unpack():
    # i, I - c_int32, c_uint32
    # c - c_shar
    # h, H = c_int16, c_uint16

    def __init__(self, wad_path):
        self.LUMP_READER_FUNCTIONS = {
        "VERTEX": self.read_vertex,
        "LINEDEF": self.read_linedef,
        "SIDEDEF": self.read_sidedef,
        "THING": self.read_thing,
        "SECTOR": self.read_sector,
        "SSECTOR": self.read_sub_sector,
        "NODE": self.read_node,
        "SEG": self.read_segment
        }
        self.file = open(wad_path, 'rb')
        self.header = self.read_header()
        self.directory = self.read_directory()
        
        
    def read_vertex(self, offset):
        x = self.read_bytes(offset, 2, 'h')
        y = self.read_bytes(offset + 2, 2, 'h')
        return Vertex(x, y)

    def read_linedef(self, offset):
        start = self.read_bytes(offset, 2, 'H')
        end = self.read_bytes(offset + 2, 2, 'H')
        flags = self.read_bytes(offset + 4, 2, 'H')
        type = self.read_bytes(offset + 6, 2, 'H')
        tag = self.read_bytes(offset + 8, 2, 'H')
        front = self.read_bytes(offset + 10, 2, 'H')
        back = self.read_bytes(offset + 12, 2, 'H')
        return Linedef(start, end, flags, type, tag, front, back)
    
    def read_sidedef(self, offset):
        _offset = (self.read_bytes(offset, 2, 'h'), self.read_bytes(offset, 2, 'h'))
        upper_t = self.read_string(offset + 4, 8)
        lower_t = self.read_string(offset + 12, 8)
        middle_t = self.read_string(offset + 20, 8)
        sector_id = self.read_bytes(offset + 28, 2, 'H')
        return Sidedef(_offset, upper_t, lower_t, middle_t, sector_id)

    def read_node(self, offset):
        start = Vertex(self.read_bytes(offset, 2, 'h'), self.read_bytes(offset + 2, 2, 'h'))
        dx = self.read_bytes(offset + 4, 2, 'h')
        dy = self.read_bytes(offset + 6, 2, 'h')
        Bbox_r = Bbox()
        Bbox_r.t = self.read_bytes(offset + 8, 2, 'h')
        Bbox_r.b = self.read_bytes(offset + 10, 2, 'h')
        Bbox_r.l = self.read_bytes(offset + 12, 2, 'h')
        Bbox_r.r = self.read_bytes(offset + 14, 2, 'h')

        Bbox_l = Bbox()
        Bbox_l.t = self.read_bytes(offset + 16, 2, 'h')
        Bbox_l.b = self.read_bytes(offset + 18, 2, 'h')
        Bbox_l.l = self.read_bytes(offset + 20, 2, 'h')
        Bbox_l.r = self.read_bytes(offset + 22, 2, 'h')

        Child_r = self.read_bytes(offset + 24, 2, 'H')
        Child_l = self.read_bytes(offset + 26, 2, 'H')
        return Node(start, dx, dy, Bbox_r, Bbox_l, Child_r, Child_l)
    
    def read_sector(self, offset):
        floor_height = self.read_bytes(offset, 2, 'h')
        ceil_height = self.read_bytes(offset + 2, 2, 'h')
        floor_texture = self.read_string(offset + 4, 8)
        ceil_texture = self.read_string(offset + 12, 8)
        light_level = self.read_bytes(offset + 20, 2, 'H')
        type = self.read_bytes(offset + 22, 2, 'H')
        tag = self.read_bytes(offset + 24, 2, 'H')
        return Sector(floor_height, ceil_height, floor_texture, ceil_texture, light_level, type, tag)


    def read_sub_sector(self, offset):
        seg_count = self.read_bytes(offset, 2, 'h')
        first_seg = self.read_bytes(offset + 2, 2, 'h')
        return SSector(seg_count, first_seg)
    
    def read_segment(self, offset):
        start = self.read_bytes(offset, 2, 'h')
        end = self.read_bytes(offset + 2, 2, 'h')
        angle = self.read_bytes(offset + 4, 2, 'h')
        linedef = self.read_bytes(offset + 6, 2, 'h')
        direction = self.read_bytes(offset + 8, 2, 'h')
        _offset = self.read_bytes(offset + 10, 2, 'h')
        return Seg(start, end, angle, linedef, direction, _offset)
    
    def read_thing(self, offset):
        pos = Vertex(self.read_bytes(offset, 2, 'h'), self.read_bytes(offset + 2, 2, 'h'))
        angle = self.read_bytes(offset + 4, 2, 'H')
        type = self.read_bytes(offset + 6, 2, 'H')
        flags = self.read_bytes(offset + 8, 2, 'H')
        return Thing(pos, angle, type, flags)
    def read_directory(self):
        directory = []
        for i in range(self.header['lump_count']):
            offset = self.header['init_offset'] + i * 16
            info = {
                "lump_offset": self.read_bytes(offset, 4, 'i'),
                "lump_size": self.read_bytes(offset + 4, 4, 'i'),
                "lump_name": self.read_string(offset + 8, 8)}
            directory.append(info)
        return directory

    def read_header(self):
        return {
            "wad_type": self.read_string(0, 4),
            "lump_count": self.read_bytes(4, 4, 'i'), 
            "init_offset": self.read_bytes(8, 4, 'i')
        }


    def read_string(self, offset, nBytes):
        return ''.join(byte.decode('utf-8') for byte in
                       self.read_bytes(
                           offset, nBytes, 'c' * nBytes))

    def read_bytes(self, offset, nBytes, format):
        self.file.seek(offset)
        data = self.file.read(nBytes)
        buffer = struct.unpack(format, data)
        if len(format) > 1: # to prevent (int,) from happening
            buffer = tuple(filter(lambda byte: byte != b'\x00', buffer))
            return buffer
        return buffer[0]
    
    def close(self): self.file.close()
    
    