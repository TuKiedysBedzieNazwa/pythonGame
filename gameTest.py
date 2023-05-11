import pygame
from game import Game

pygame.init()

width, height = 840, 1000 #1340
display = pygame.display.set_mode((width, height))
acceleration = 0


y = 400
x = 400


while True:
    Game(width, height, display, acceleration, x, y)