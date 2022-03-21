from vec import *

#server
class Physics:
    def __init__(self, pos):
        self.pos = pos
        self.velocity = Vec2(0, 0)
        self.acceleration = Vec2(0, 0)
        self.resistance = Vec2(0.97, 0.97)
    
    def update(self):
        self.pos = getAddVec2(self.pos, self.velocity)
        self.velocity = getAddVec2(self.velocity, self.acceleration)
        self.velocity = getMulVec2(self.velocity, self.resistance)

class Player:
    def __init__(self, pos, spriteID):
        self.physics = Physics(pos)
        self.spriteID = spriteID

class Bullet:
    def __init__(self, pos):
        self.physics = Physics(pos)

class Action:
    def __init__(self, tag):
        self.tag = tag
        self.down = False
        self.downed = False
        self.upped = False

class ServerSprite:
    def __init__(self, pos, size, ID):
        self.pos = pos;
        self.size = size;
        self.ID = ID;

#client
class Sprite:
    def __init__(self, pos, size):
        self.pos = pos;
        self.size = size;

class Key:
    def __init__(self):
        self.down = False
        self.downed = False
        self.downed = False

#shared
