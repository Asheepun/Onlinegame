import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect((socket.gethostname(), 1233))

import sys
import time
import sdl2.ext

FRAME_TIME = 1 / 60

sdl2.ext.init()

window = sdl2.ext.Window("Hello World!", size=(640, 480))
window.show()

factory = sdl2.ext.SpriteFactory(sdl2.ext.SOFTWARE)
sprite = factory.from_image("atlas.png")

spriterenderer = factory.create_sprite_render_system(window)
spriterenderer.render(sprite)

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
    spriterenderer.render(sprite)


    msg = s.recv(1024)

    print(msg.decode("utf-8"))

    stopTime = time.perf_counter()
    deltaTime = startTime - stopTime

    sleepTime = FRAME_TIME - deltaTime
    if(sleepTime < 0):
        sleepTime = 0

    time.sleep(sleepTime)
    #print("h")
    
    window.refresh()

