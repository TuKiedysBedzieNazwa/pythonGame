import pygame, sys
import tensorflow as tf
from functions import renderBlocks, collisionCheck, config

def Game():

    width, height, display, x, y, acceleration = config()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]:
                sys.exit()
            elif pygame.key.get_pressed()[pygame.K_UP] and acceleration == 0:
                acceleration = -5
        if pygame.key.get_pressed()[pygame.K_LEFT] and x > 0:
            x -= 3
        if pygame.key.get_pressed()[pygame.K_RIGHT] and x < width - 40:
            x += 3
        display.fill((255, 255, 255))

        y += acceleration

        if acceleration < 10: acceleration += 0.1 #on se cały czas dodaje 0.1
        if y >= height - 40: acceleration = 0
        
        #if y > height - 39: y = height - 550  //Do poprawy, kostka wbija się w ziemie :c




        pygame.draw.circle(display, (0, 0, 0), [x - 80, y + 20], 20)
        pygame.draw.rect(display, (0, 0, 0), pygame.Rect(x, y, 40, 40))
        renderBlocks(display)

        if collisionCheck(x, y): acceleration = 0

        pygame.time.Clock().tick(70)
        pygame.display.flip()

Game()
