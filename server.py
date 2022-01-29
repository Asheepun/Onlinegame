import socket
import time

class Vec2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

def getAddVec2(v1, v2):
    return Vec2(v1.x + v2.x, v1.y + v2.y)

def getMulVec2(v1, v2):
    return Vec2(v1.x * v2.x, v1.y * v2.y)

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
    def __init__(self, pos):
        self.physics = Physics(pos)

class Bullet:
    def __init__(self, pos):
        self.physics = Physics(pos)

players = [];
bullets = [];

players.append(Player(Vec2(100, 100)))

frameTime = 1 / 60

startTime = 0
stopTime = 0
deltaTime = 0

programBeginTime = time.perf_counter()

while True:

    startTime = time.perf_counter()

    passedTime = time.perf_counter() - programBeginTime

    print(passedTime)

    #update game
    
    for player in players:
        player.physics.update()
    
    for bullet in bullets:
        bullet.physics.update()

    #handle timing

    stopTime = time.perf_counter()

    deltaTime = stopTime - startTime

    time.sleep(frameTime - deltaTime)

# create the socket
# AF_INET == ipv4
# SOCK_STREAM == TCP
#s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#s.bind((socket.gethostname(), 1235))

#s.listen(5)

#while True:
    # now our endpoint knows about the OTHER endpoint.
    #clientsocket, address = s.accept()
    #print(f"Connection from {address} has been established.")

    #clientsocket.send(bytes("Hey there!!!","utf-8"))


#print("hello")
