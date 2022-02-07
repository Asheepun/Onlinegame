import socket
import threading

from vec import *

import sys
import time
import sdl2
import sdl2.ext

FRAME_TIME = 1 / 60

class Sprite:
    def __init__(self, pos, size):
        self.pos = pos;
        self.size = size;

#setup keys
class Key:
    def __init__(self):
        self.down = False
        self.downed = False
        self.downed = False

    
keys = []
for i in range(0, 1000):
    keys.append(Key())

#setup sprites and rendering

sdl2.ext.init()

window = sdl2.ext.Window("Hello World!", size=(640, 480))
window.show()

factory = sdl2.ext.SpriteFactory(sdl2.ext.SOFTWARE)
texture = factory.from_image("sprites/person.png")#, size=(50, 50))
backgroundTexture = factory.from_color((0, 0, 0), size=(640, 480))
#texture = factory.from_color((255, 255, 255), size=(50, 50))

spriterenderer = factory.create_sprite_render_system(window)

sprites = []

sprites.append(Sprite(Vec2(20, 20), Vec2(50, 50)))

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

serverSocket.connect((socket.gethostname(), 1235))

#setup server connection
def serverThreadFunction():

    while True:

        msg = serverSocket.recv(1024)
        msgText = msg.decode("utf-8")

        coords = msgText.split(" ");

        print(coords)

        sprites[0].pos = Vec2(int(coords[0]), int(coords[1]))

thread = threading.Thread(target=serverThreadFunction)

thread.start()

running = True

while running:

    startTime = time.perf_counter()
    events = sdl2.ext.get_events()

    for i in range(0, 1000):
        keys[i].downed = False;
        keys[i].upped = False;

    #handle events
    for event in events:
        if event.type == sdl2.SDL_QUIT:
            running = False
            break
        if(event.type == sdl2.SDL_KEYDOWN
        and event.key.keysym.sym < 1000):
            if(keys[event.key.keysym.sym].down == False):
                keys[event.key.keysym.sym].downed = True;
            keys[event.key.keysym.sym].down = True;

        if(event.type == sdl2.SDL_KEYUP
        and event.key.keysym.sym < 1000):
            if(keys[event.key.keysym.sym].down):
                keys[event.key.keysym.sym].upped = True;
            keys[event.key.keysym.sym].down = False;

    #handle input, send to server
    if keys[sdl2.SDLK_w].downed:
        serverSocket.send(bytes("up downed", "utf-8"))
    if keys[sdl2.SDLK_s].downed:
        serverSocket.send(bytes("down downed", "utf-8"))
    if keys[sdl2.SDLK_a].downed:
        serverSocket.send(bytes("left downed", "utf-8"))
    if keys[sdl2.SDLK_d].downed:
        serverSocket.send(bytes("right downed", "utf-8"))
    if keys[sdl2.SDLK_w].upped:
        serverSocket.send(bytes("up upped", "utf-8"))
    if keys[sdl2.SDLK_s].upped:
        serverSocket.send(bytes("down upped", "utf-8"))
    if keys[sdl2.SDLK_a].upped:
        serverSocket.send(bytes("left upped", "utf-8"))
    if keys[sdl2.SDLK_d].upped:
        serverSocket.send(bytes("right upped", "utf-8"))

    #update

    #render
    spriterenderer.render(backgroundTexture, 0, 0)
    spriterenderer.render(texture, sprites[0].pos.x, sprites[0].pos.y)

    #handle frame time

    stopTime = time.perf_counter()
    deltaTime = startTime - stopTime

    sleepTime = FRAME_TIME - deltaTime
    if(sleepTime < 0):
        sleepTime = 0

    time.sleep(sleepTime)
    #print("h")
    
    window.refresh()

