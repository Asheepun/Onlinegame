class Vec2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

def getAddVec2(v1, v2):
    return Vec2(v1.x + v2.x, v1.y + v2.y)

def getMulVec2(v1, v2):
    return Vec2(v1.x * v2.x, v1.y * v2.y)

