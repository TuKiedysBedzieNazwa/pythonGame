import pygame

blockCords=[
    [550, 1000], #dół
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
