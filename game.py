import pygame, time, math, random
from actionSpace import actionSpace

class Game():
    def __init__(self) -> None:
        super(Game, self).__init__()
        self.action_space = actionSpace()


        self.acceleration = 0
        self.width, self.height = 840, 1340
        self.x, self.y  = 30, self.height - 40
        self.display = None

        self.currentTime: int = 0
        self.frames: int = 0

        self.text = pygame.font.Font('freesansbold.ttf', 18)

        self.blocks = [pygame.Rect(200, 1310, 100, 50)]
        self.generateBlocks()
        self.done: bool = True

    def step(self, action) -> None:

        if self.acceleration == 0:
            self.acceleration = action[1] * -5
        self.x += action[0] * 3
        self.x -= action[2] * 3
        self.render()

        return action[0]

    def reset(self):
        return True
    
    def render(self) -> None:
        self.generateFrame()
        self.updateScreen()

    def close(self) -> None:
        if self.display is not None:
            pygame.display.quit()
            pygame.quit()
            self.display = None


    def debug(self) -> None:
        while self.done:

            self.generateFrame()
            # self.mouseDebug()
            self.frameMonitor()

            pygame.time.Clock().tick(140)

            self.updateScreen()

            if pygame.key.get_pressed()[pygame.K_UP] and self.acceleration == 0 and self.touchGround():
                self.acceleration = -5
            elif pygame.key.get_pressed()[pygame.K_LEFT] and self.x > 0:
                self.x -= 3
            elif pygame.key.get_pressed()[pygame.K_RIGHT] and self.x < self.width - 40:
                self.x += 3
            for event in pygame.event.get():
                if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]:
                    self.done = False
                    self.close()

    def generateFrame(self) -> None:
        if self.display is None:
            pygame.init()
            pygame.display.init()
            pygame.display.set_caption('Simple Game')
            self.display = pygame.display.set_mode((self.width, self.height))

        self.display.fill((255, 255, 255))

        self.y += self.acceleration

        if self.acceleration < 10: self.acceleration += 0.1
        if self.y >= self.height - 40: self.acceleration = 0

        # pygame.draw.circle(display, (0, 0, 0), [x - 80, y + 20], 20)
        pygame.draw.rect(self.display, (0, 0, 0), pygame.Rect(self.x, self.y, 40, 40))
        self.renderBlocks()

    def touchGround(self) -> bool:
        for block in self.blocks:
            print(block[1])
            if self.y - 40 > block[1] and self.y - 40 < block[0] + block[1] and self.x > block[0] and self.x < block[0] + block[2]:
                self.acceleration = 0
                return False

        return True

    def touchLeft(self) -> bool:
        return True

    def touchRight(self) -> bool:
        return True

    def touchBottom(self) -> bool:
        return True

    def updateScreen(self) -> None:
        pygame.event.pump()
        # pygame.display.flip()
        pygame.display.update()

    def generateBlocks(self) -> None:
        howMany: int = 15
        toRight: bool = True
        for i in range(howMany - 1, 0, -1):

            y: float = self.height * i / howMany - 50 + random.randint(-10, 10)

            if self.blocks[-1][0] < 270 and not toRight:
                if random.random() > 0.7 and self.blocks[-1][0] != 0:
                    self.blocks.append(pygame.Rect(0, round(y), 100, 50))
                    continue
                toRight = True
            elif self.blocks[-1][0] > self.width - 370 and toRight:
                if random.random() > 0.7 and self.blocks[-1][0] != self.width - 100:
                    self.blocks.append(pygame.Rect(self.width - 100, round(y), 100, 50))
                    continue
                toRight = False

            if toRight:
                x: int = random.randint(self.blocks[-1][0] + 170, self.blocks[-1][0] + 250)
            else:
                x: int = random.randint(self.blocks[-1][0] - 250, self.blocks[-1][0] - 170)

            self.blocks.append(pygame.Rect(x, round(y), 100, 50))

        for block in self.blocks:
            print(block)
        print(len(self.blocks))

    def renderBlocks(self) -> None:
        if self.display is not None:
            for rect in self.blocks:
                pygame.draw.rect(self.display, (50, 50, 55), rect)

    def mouseDebug(self) -> None:
        if self.display is not None:
            x, y = pygame.mouse.get_pos()
            rect = pygame.Rect(x, y, 20, 20)
            if rect.collidelist(self.blocks) != -1:
                pygame.draw.rect(self.display, (255, 0, 0), rect)
            else:
                pygame.draw.rect(self.display, (0, 255, 0), rect)

    def debugMonitor(self):
        return True

    def frameMonitor(self) -> None:
        if self.display is not None:
            self.frames += 1
            if self.currentTime != math.floor(time.time()):
                # text = pygame.font.Font('freesansbold.ttf', 18).render(str(self.frames), True, (0, 0, 0), (255, 255, 255))
                self.frames = 0
                self.currentTime = math.floor(time.time())
            
            self.display.blit(self.text.render(str(self.frames), True, (0, 0, 0), (255, 255, 255)), [10, 10])

env = Game()

env.debug()