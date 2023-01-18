import pygame

def config():
    pygame.init()

    width, height = 840, 1000 #1340

    display = pygame.display.set_mode((width, height))
    x = 400
    y = height - 40

    acceleration = 0

    return width, height, display, x, y, acceleration


blockCords=[
    [200, 1240], #dół
    [0, 1130],
    [280, 1050],
    [550, 1000],
    [740, 900],
    [500, 800],
    [230, 780],
    [20, 720],
    [290, 600],
    [520, 500],
    [710, 430],
    [500, 300],
    [300, 150],
    [0, 70] #góra 
]

def renderBlocks(display):
    for i in blockCords:
        pygame.draw.rect(display, (50, 50, 55), pygame.Rect(i[0], i[1], 100, 100))

def collisionCheck(x, y):
    
    for i in blockCords:
        if i[0] - 40 <= x and i[0] + 100 >= x and i[1] - 40 <= y and i[1] + 20 >= y: return True
    return False
