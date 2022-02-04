import socket
import threading
import time

from vec import *

# AF_INET == ipv4
# SOCK_STREAM == TCP
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind((socket.gethostname(), 1234))

s.listen(5)

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

class Action:
    def __init__(self, tag):
        self.tag = tag
        self.down = False
        self.downed = False
        self.upped = False

actions = [
    Action("up"),
    Action("down"),
    Action("left"),
    Action("right"),
]

def getAction(tag):
    for action in actions:
        if(action.tag == tag):
            return action

players = [];
bullets = [];

players.append(Player(Vec2(100, 100)))

FRAME_TIME = 1 / 60

startTime = 0
stopTime = 0
deltaTime = 0

programBeginTime = time.perf_counter()

playerCount = 0


while playerCount < 1:
    clientSocket, address = s.accept()
    print("Connection from {address} has been established.")
    playerCount += 1

#setup event recieve loop
def eventRecieveFunction():
    while True:
        msg = clientSocket.recv(1024)
        msgText = msg.decode("utf-8")

        event = msgText.split(" ")

        for action in actions:
            if(action.tag == event[0]):
                if(event[1] == "downed"):
                    action.down = True
                if(event[1] == "upped"):
                    action.down = False


thread = threading.Thread(target=eventRecieveFunction)

thread.start()

while True:

    startTime = time.perf_counter()

    passedTime = time.perf_counter() - programBeginTime

    #update game

    players[0].physics.velocity.x = 0;
    players[0].physics.velocity.y = 0;

    if(getAction("up").down):
        players[0].physics.velocity.y = -1;
    if(getAction("down").down):
        players[0].physics.velocity.y = 1;
    if(getAction("left").down):
        players[0].physics.velocity.x = -1;
    if(getAction("right").down):
        players[0].physics.velocity.x = 1;
    
    for player in players:
        player.physics.update()
    
    for bullet in bullets:
        bullet.physics.update()

    #server stuff
    clientSocket.send(bytes(str(int(players[0].physics.pos.x)) + " " + str(int(players[0].physics.pos.y)), "utf-8"))

    #handle timing

    stopTime = time.perf_counter()

    deltaTime = stopTime - startTime

    sleepTime = FRAME_TIME - deltaTime
    if(sleepTime < 0):
        sleepTime = 0

    time.sleep(sleepTime)

