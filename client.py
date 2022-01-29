import socket
import threading

import sys
import time
import sdl2
import sdl2.ext

FRAME_TIME = 1 / 60

class Vec2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

def getAddVec2(v1, v2):
    return Vec2(v1.x + v2.x, v1.y + v2.y)

def getMulVec2(v1, v2):
    return Vec2(v1.x * v2.x, v1.y * v2.y)

class Sprite:
    def __init__(self, pos, size):
        self.pos = pos;
        self.size = size;

#setup sprites and rendering

sdl2.ext.init()

window = sdl2.ext.Window("Hello World!", size=(640, 480))
window.show()

factory = sdl2.ext.SpriteFactory(sdl2.ext.SOFTWARE)
#texture = factory.from_image("atlas.png", size=(50, 50))
backgroundTexture = factory.from_color((0, 0, 0), size=(640, 480))
texture = factory.from_color((255, 255, 255), size=(50, 50))

spriterenderer = factory.create_sprite_render_system(window)

sprites = []

sprites.append(Sprite(Vec2(20, 20), Vec2(50, 50)))

#setup server connection
def serverThreadFunction():

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.connect((socket.gethostname(), 1232))

    while True:

        msg = s.recv(1024)
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
    for event in events:
        if event.type == sdl2.SDL_QUIT:
            running = False
            break

    if 0:
        running = False

    spriterenderer.render(backgroundTexture, 0, 0)
    spriterenderer.render(texture, sprites[0].pos.x, sprites[0].pos.y)

    stopTime = time.perf_counter()
    deltaTime = startTime - stopTime

    sleepTime = FRAME_TIME - deltaTime
    if(sleepTime < 0):
        sleepTime = 0

    time.sleep(sleepTime)
    #print("h")
    
    window.refresh()

