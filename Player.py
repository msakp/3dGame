class Player:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.XAngle = 0
        self.YAngle = 0
    def getPos(self): return self.x, self.y, self.z
    def getAngle(self): return self.XAngle, self.YAngle
