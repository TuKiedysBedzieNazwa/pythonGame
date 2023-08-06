import pygame, random, gym, math
from gym import spaces
import numpy as np
from vectors import Vectors
from debug import Debug
from scoreboard import Scoreboard

class Game(gym.Env, Vectors, Debug, Scoreboard):
    def __init__(self) -> None:
        # super(Game, self).__init__()

        Vectors.__init__(self)
        # Debug.__init__(self)
        Scoreboard.__init__(self)

        obsLow  = np.array([0,   0,    0, 0, 0, 0, 0,    0,   0,    0,   0,    0,   0,    0,   0,    0, 0])
        obsHigh = np.array([840, 1400, 1, 1, 1, 1, 2000, 840, 1400, 840, 1400, 840, 1400, 840, 1400, 1, 1])

        self.observation_space = spaces.Box(low=obsLow, high=obsHigh, shape=(17,))

        self.action_space = spaces.Discrete(3)

        self.acceleration: float = 0
        self.width, self.height = 840, 1340
        self.x, self.y  = 30, self.height - 200
        self.display = None
        self.text = None

        self.player = None
        self.moveUp: bool = False
        self.moveDown: bool = False

        self.touchGround: bool = False
        self.touchRight: bool = False
        self.touchLeft: bool = False
        self.touchBottom: bool = False

        self.blocks = [pygame.Rect(0, self.height - 160, 840, 160), pygame.Rect(200, self.height - 200, 100, 40)]
        self.stars = [pygame.Rect(83, 1130, 34, 40), pygame.Rect(233, 1090, 34, 40)]
        self.animationProgress: int = 0
        self.buildToRight: bool = True
        # self.generateBlocks()
        self.done: bool = False
        self.stop = 0
        self.temporaryReward: int = 0
        self.modelReward: int = 0


    def step(self, action) -> None:

        if action == 1 and self.acceleration == 0:
            self.acceleration = -5
        elif action == 2 and self.x > 0 and not self.touchLeft:
            self.x -= 3
        elif action == 0 and self.x < self.width - 40 and not self.touchRight:
            self.x += 3
        self.render()

        return [self.getObservation(), self.temporaryReward, self.done, {}]

    def reset(self):
        if self.player == None:
            self.player = pygame.Rect(self.x, self.y, 40, 40)
        self.modelReward = 0
        self.stop = 0
        self.done = False
        self.resetScore()
        self.x, self.y  = 30, self.height - 200
        self.acceleration = 0
        self.animationProgress = 0
        self.moveDown = False
        self.moveUp = False
        self.blocks = [pygame.Rect(0, self.height - 160, 840, 160), pygame.Rect(200, self.height - 200, 100, 40)]
        self.stars = [pygame.Rect(93, 1130, 34, 40), pygame.Rect(233, 1090, 34, 40)]
        self.generateBlocks()
        
        self.nearestBlocks()
        # self.nearestStar()
        return self.getObservation()

    def render(self, mode="human") -> None:
        self.generateFrame()
        self.updateScreen()

    def close(self) -> None:
        if self.display is not None:
            pygame.display.quit()
            pygame.quit()
            self.display = None


    def generateFrame(self) -> None:
        if self.display is None:
            pygame.init()
            pygame.display.init()
            pygame.display.set_caption('Simple Game')
            self.display = pygame.display.set_mode((self.width, self.height))
            self.text = pygame.font.Font('freesansbold.ttf', 18)

        self.display.fill((115, 131, 255))

        if not self.moveDown: self.y += self.acceleration
        if self.acceleration < 10: self.acceleration += 0.1

        self.player = pygame.Rect(self.x, self.y, 40, 40)

        self.renderScore()
        self.renderBlocks()
        # self.starAnimation()
        
        self.temporaryRewardCheck()
        self.nearestStar()
        self.nearestBlocks()

        self.collisionCheck()

        # pygame.draw.circle(display, (0, 0, 0), [x - 80, y + 20], 20)
        pygame.draw.rect(self.display, (0, 0, 0), self.player)


        if self.y < self.height / 2:
            self.moveUp = True
            self.y += 2
        elif self.y > self.height - 180:
            self.moveDown = True
            self.y += 3
            if self.y > self.height + 50: self.reset()
        else:
            self.moveDown = False
            self.moveUp = False
        
        self.stop += 1
        # if self.stop % 100 == 0: self.temporaryReward -= 1
        if self.stop == 1000 or self.modelReward < -50: self.done = True
        self.display.blit(self.text.render(f"reward: {self.modelReward}", True, (0, 0, 0), (255, 255, 255)), [10, 40])
        self.display.blit(self.text.render(f"time: {self.stop}", True, (0, 0, 0), (255, 255, 255)), [10, 60])

        for i, val in enumerate(self.getObservation()):
            self.display.blit(self.text.render(f"{val}", True, (0, 0, 0), (255, 255, 255)), [10, 80 + i * 15])


    def updateScreen(self) -> None:
        pygame.event.pump()
        # pygame.display.flip()
        pygame.display.update()

    def collisionCheck(self):
        arr = [False, False, False, False]

        if self.player != None:
            colidate = self.player.collidelist(self.stars)
            if colidate != -1:
                self.stars.pop(colidate)
                self.addScore()
                self.temporaryReward += 100

        for block in self.blocks:
            if self.y + 40 >= block[1] and self.y < block[1] + block[3] / 2 and self.x + 40 > block[0] and self.x < block[0] + block[2]:
                self.acceleration = 0
                self.y = block[1] - 40
                arr[0] = True
            elif self.y + 40 > block[1] + block[3] / 2 and self.y <= block[1] + block[3] and self.x + 40 > block[0] and self.x < block[0] + block[2]:
                self.y = block[1] + block[3]
                self.acceleration = -self.acceleration / 2
                arr[1] = True
            elif self.y + 40 > block[1] and self.y < block[1] + block[3] and self.x + 40 > block[0] + block[2] / 2 and self.x <= block[0] + block[2] + 2:
                self.x = block[0] + block[2]
                arr[2] = True
            elif self.y + 40 > block[1] and self.y < block[1] + block[3] and self.x + 40 >= block[0] - 2 and self.x < block[0] + block[2] / 2:
                self.x = block[0] - 40
                arr[3] = True

        self.touchGround, self.touchBottom, self.touchLeft, self.touchRight = arr
        return arr[0], arr[1], arr[2], arr[3]

    def generateBlocks(self) -> None:
        for i in range(12):
            self.generateBlock()

    def generateBlock(self) -> None:
        y: float = self.blocks[-1][1] - 110 + random.randint(-10, 10)

        if self.blocks[-1][0] < 270 and not self.buildToRight:
            if random.random() > 0.7 and self.blocks[-1][0] != 0:
                self.blocks.append(pygame.Rect(0, round(y), 100, 50))
                return
            self.buildToRight = True
        elif self.blocks[-1][0] > self.width - 370 and self.buildToRight:
            if random.random() > 0.7 and self.blocks[-1][0] != self.width - 100:
                self.blocks.append(pygame.Rect(self.width - 100, round(y), 100, 50))
                return
            self.buildToRight = False

        if self.buildToRight:
            x: int = random.randint(self.blocks[-1][0] + 170, self.blocks[-1][0] + 250)
        else:
            x: int = random.randint(self.blocks[-1][0] - 250, self.blocks[-1][0] - 170)

        self.blocks.append(pygame.Rect(x, round(y), 100, 50))
        if random.random() > 0.1:
            self.stars.append(pygame.Rect(x + 33, round(y) - 50, 34, 40))

    def renderBlocks(self) -> None:
        for rect in self.blocks:
            if self.moveUp: rect[1] += 2
            elif self.moveDown: rect[1] -= 10
            pygame.draw.rect(self.display, (50, 50, 55), rect)

        if self.blocks[-1][1] > 200:
            self.generateBlock()
            self.blocks.pop(0)

        for star in self.stars:
            if self.moveUp: star[1] += 2
            elif self.moveDown: star[1] -= 10
            pygame.draw.rect(self.display, (255, 214, 0), star)

    def starAnimation(self) -> None:
        if self.animationProgress == 100: self.animationProgress = 0
        if self.animationProgress % 5 == 0:
            for star in self.stars:
                if self.animationProgress >= 50:
                    star[1] += 1
                else:
                    star[1] -= 1

        self.animationProgress += 1

    def temporaryRewardCheck(self) -> None:
        self.modelReward += self.temporaryReward
        self.temporaryReward = 0

        # if self.y < self.stars[0][1] and self.acceleration != 0:
            # self.temporaryReward -= 1
        if self.x < 10 or self.x > self.width - 50:
            self.temporaryReward -= 1
        if self.touchGround and self.touchLeft:
            self.temporaryReward -= 1
        elif self.touchGround and self.touchRight:
            self.temporaryReward -= 1
        elif self.touchBottom:
            self.temporaryReward -= 1

    def getObservation(self):
        [dist, [sx,sy]] = self.getNearestStar()
        [b1, b2, b3, b4] = self.getNearestBlocks()
        return [self.x, self.y, self.touchGround, self.touchRight, self.touchLeft, self.touchBottom, dist, sx, sy, b1[0], b1[1], b2[0], b2[1], b3[0], b3[1], self.moveUp, self.moveDown]


# Game().debug()