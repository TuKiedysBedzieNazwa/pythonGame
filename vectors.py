import math, pygame

class Vectors:
    def __init__(self) -> None:

        self.nearestStarDist = []
        self.nearestBlocksDist = []

    def nearestStar(self) -> None:
        starLen = len(self.stars)

        if starLen == 0:
            self.nearestStarDist = 0
            return 0
        elif starLen > 5: starLen = 5

        arr = []
        nearestCords = []
        for i in range(starLen):
            x = abs(self.x + self.player[2] / 2 - self.stars[i][0] + self.stars[i][2] / 2)
            y = abs(self.y + self.player[3] / 2 - self.stars[i][1] + self.stars[i][3] / 2)
            nearestCords.append([self.stars[i][0] + self.stars[i][2] / 2, self.stars[i][1] + self.stars[i][3] / 2])

            arr.append([math.sqrt(math.pow(x, 2) + math.pow(y, 2)), [self.stars[i][0] + self.stars[i][2] / 2, self.stars[i][1] + self.stars[i][3] / 2]])

        arr.sort()
        self.nearestStarDist = arr[0]
        self.line(self.x + self.player[2] / 2, self.y + self.player[3] / 2, arr[0][1][0], arr[0][1][1], (0, 255, 0))

    def nearestBlocks(self):
        arr = []

        for block in self.blocks:
            x = abs(self.x + self.player[2] / 2 - block[0] + block[2] / 2)
            y = abs(self.y + self.player[3] / 2 - block[1] + block[3] / 2)
            arr.append([math.sqrt(math.pow(x, 2) + math.pow(y, 2)), [block[0] + block[2] / 2, block[1] + block[3] / 2]])

        arr.sort()
        self.nearestBlocksDist = [arr[0][1], arr[1][1], arr[2][1], arr[3][1]]

        for i in range(3):
            self.line(self.x + self.player[2] / 2, self.y + self.player[3] / 2, arr[i][1][0], arr[i][1][1], (0, 0, 255))


    def getNearestStar(self):
        return self.nearestStarDist

    def getNearestBlocks(self):
        return self.nearestBlocksDist

    def line(self, x1: int, y1: int, x2: int, y2: int, color) -> None:
        pygame.draw.line(self.display, color, (x1, y1),(x2, y2), width=3)
