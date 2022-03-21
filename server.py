import socket
import threading
import time

from vec import *
from classes import *
from functions import *

#connect to socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind((socket.gethostname(), 1235))

s.listen(5)

#global variables
actions = [
    Action("up"),
    Action("down"),
    Action("left"),
    Action("right"),
]

players = []
bullets = []
sprites = []

availableID = 0

FRAME_TIME = 1 / 60

startTime = 0
stopTime = 0
deltaTime = 0

programBeginTime = time.perf_counter()

playerCount = 0

#local functions

def eventReceiveFunction():
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

def getAction(tag):
    for action in actions:
        if(action.tag == tag):
            return action

def addSprite(pos, size):
    global availableID
    sprites.append(ServerSprite(pos, size, availableID))
    availableID += 1
    return availableID - 1

def getSprite(ID):
    for sprite in sprites:
        if(sprite.ID == ID):
            return sprite;

def addPlayer(pos):
    players.append(Player(pos, addSprite(pos, Vec2(40, 40))))
    

#MAIN PROGRAM

addPlayer(Vec2(100, 100))

addSprite(Vec2(200, 100), Vec2(20, 20))

#wait for players to connect
while playerCount < 1:
    clientSocket, address = s.accept()
    print("Connection from {address} has been established.")
    playerCount += 1

#start event receive thread
thread = threading.Thread(target=eventReceiveFunction)
thread.start()

print("Started game loop.")

#start game loop
while True:

    startTime = time.perf_counter()

    passedTime = time.perf_counter() - programBeginTime

    #update game
    players[0].physics.velocity.x = 0
    players[0].physics.velocity.y = 0

    if(getAction("up").down):
        players[0].physics.velocity.y = -1
    if(getAction("down").down):
        players[0].physics.velocity.y = 1
    if(getAction("left").down):
        players[0].physics.velocity.x = -1
    if(getAction("right").down):
        players[0].physics.velocity.x = 1
    
    for player in players:
        player.physics.update()
    
    for bullet in bullets:
        bullet.physics.update()

    for player in players:
        sprite = getSprite(player.spriteID)
        sprite.pos = player.physics.pos

    #server stuff
    stringToSend = ""
    for sprite in sprites:
        stringToSend += str(int(sprite.pos.x)) + "," + str(int(sprite.pos.y)) + "," + str(int(sprite.size.x)) + "," + str(int(sprite.size.y)) + "."

    bytesToSend = bytes(stringToSend, "utf-8")
    clientSocket.send(bytesToSend)

    #handle timing

    stopTime = time.perf_counter()

    deltaTime = stopTime - startTime

    sleepTime = FRAME_TIME - deltaTime
    if(sleepTime < 0):
        sleepTime = 0

    time.sleep(sleepTime)
