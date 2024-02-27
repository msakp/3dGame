from wadReader import WadReader
from numba import jit, njit

class WadData:
    MAP_INDICIES = {
        "THINGS": 1, "LINEDEFS": 2, "SIDEDEFS": 3, "VERTEXES": 4, "SEGS": 5,
        "SSECTORS": 6, "NODES": 7, "SECTORS": 8, "REJECT": 9, "BLOCKMAP": 10
    }
    LINEDEF_FLAGS = {
        "BLOCKING": 1, "BLOCK_MONSTERS": 2, "TWO_SIDED": 4, "DONT_PEG_TOP": 8,
        "DONT_PEG_BOTTOM": 16, "SECRET": 32, "SOUND_BLOCK": 64, "DONT_DRAW": 128, "MAPPED": 256
    }

    def __init__(self, engine, map_name):
        self.reader = WadReader(engine.wad_path)
        self.map_index = self.get_lump_index(map_name)
        self.vertecies = self.get_lump_data(
            "VERTEX", 
            self.map_index + self.MAP_INDICIES["VERTEXES"],
            4
        )
        self.linedefs = self.get_lump_data(
            "LINEDEF",
            self.map_index + self.MAP_INDICIES["LINEDEFS"],
            14
        )

        self.sidedefs = self.get_lump_data(
            "SIDEDEF",
            self.map_index + self.MAP_INDICIES["SIDEDEFS"],
            30
         )


        self.things = self.get_lump_data(
            "THING",
            self.map_index + self.MAP_INDICIES["THINGS"],
            10
        )

        self.sectors = self.get_lump_data(
            "SECTOR",
            self.map_index + self.MAP_INDICIES["SECTORS"],
            26
        )

        self.ssectors = self.get_lump_data(
            "SSECTOR",
            self.map_index + self.MAP_INDICIES["SSECTORS"],
            4
        )
        self.nodes = self.get_lump_data(
            "NODE",
            self.map_index + self.MAP_INDICIES["NODES"],
            28
        )
        self.segs = self.get_lump_data(
            "SEG",
            self.map_index + self.MAP_INDICIES["SEGS"],
            12
        )



        self.reader.close() 

    
    def get_lump_data(self, flag, lump_index, nBytes, header_length=0):
        read_data = self.reader.LUMP_READER_FUNCTIONS[flag]

        lump_info = self.reader.directory[lump_index]
        size = lump_info["lump_size"] // nBytes
        data = []
        for i in range(size):
            offset = lump_info["lump_offset"] + i * nBytes + header_length
            data.append(read_data(offset))
        return tuple(data)

    def get_lump_index(self, lump_name):
        for index, info in enumerate(self.reader.directory):
            if lump_name in info.values():
                return index
