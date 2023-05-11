import pygame, sys
from functions import renderBlocks, collisionCheck

def Game(width, height, display, acceleration, x , y):

    for event in pygame.event.get():
        if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]:
            sys.exit()
    if pygame.key.get_pressed()[pygame.K_UP] and acceleration == 0:
        acceleration = -5
    elif pygame.key.get_pressed()[pygame.K_LEFT] and x > 0:
        x -= 3
    elif pygame.key.get_pressed()[pygame.K_RIGHT] and x < width - 40:
        x += 3



    display.fill((255, 255, 255))

    y += acceleration

    if acceleration < 10: acceleration += 0.1 #on se cały czas dodaje 0.1
    if y >= height - 40: acceleration = 0


    pygame.draw.circle(display, (0, 0, 0), [x - 80, y + 20], 20)
    pygame.draw.rect(display, (0, 0, 0), pygame.Rect(x, y, 40, 40))
    renderBlocks(display)

    if collisionCheck(x, y): acceleration = 0

    # pygame.time.Clock().tick(70)
    pygame.display.flip()
