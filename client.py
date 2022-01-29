import pygame

pygame.init()

screen = pygame.display.set_mode([500, 500])

running = True

while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            running = False

    screen.fill((255, 255, 255))

    pygame.draw.circle(screen, (0, 0, 255), (250, 250), 75)

    pygame.display.flip()

pygame.quit()

#import socket

#s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#s.connect((socket.gethostname(), 1235))

#msg = s.recv(1024)

#print(msg.decode("utf-8"))
