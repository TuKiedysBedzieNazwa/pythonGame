import pygame, sys


def Game():

    pygame.init()

    width, height = 840, 1340

    display = pygame.display.set_mode((width, height))
    x = 400
    y = height - 40

    acceleration = 0

    def renderBlocks(x, y): return pygame.draw.rect(display, (50, 50, 55), pygame.Rect(x, y, 100, 100))

    cords=[
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

    def collisionCheck(x, y):
        for i in cords:
            if i[0] - 40 <= x and i[0] + 100 >= x and i[1] - 40 <= y and i[1] + 20 >= y: return True

        return False


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            elif pygame.key.get_pressed()[pygame.K_ESCAPE]: sys.exit()
            elif pygame.key.get_pressed()[pygame.K_UP] and acceleration == 0:
                acceleration = -5
        if pygame.key.get_pressed()[pygame.K_LEFT] and x > 0:
            x -= 3
        if pygame.key.get_pressed()[pygame.K_RIGHT] and x < width - 40:
            x += 3

        display.fill((255, 255, 255))

        pygame.draw.rect(display, (0, 0, 0), pygame.Rect(x, y, 40, 40))

        y += acceleration

        if acceleration < 10: acceleration += 0.1
        if y > height - 40: acceleration = 0

        if y > height: y = height


        for i in cords:
            renderBlocks(i[0], i[1])

        if collisionCheck(x, y): acceleration = 0


        pygame.time.Clock().tick(120)
        pygame.display.flip()
