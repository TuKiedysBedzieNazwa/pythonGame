import pygame, time, math

class Debug:

    def __init__(self) -> None:
        self.currentTime: int = 0
        self.frames: int = 0
        self.framesMax: str = "69"

    def debug(self) -> None:
        while not self.done:

            self.generateFrame()
            # self.mouseDebug()
            # self.debugMonitor()
            self.debugMonitor2()
            self.frameMonitor()

            pygame.time.Clock().tick(150)

            self.updateScreen()

            if pygame.key.get_pressed()[pygame.K_UP] and self.acceleration == 0:
                # self.step([0, 1, 0])
                self.acceleration -= 5
            elif pygame.key.get_pressed()[pygame.K_LEFT] and self.x > 0 and not self.touchLeft:
                # self.step([0, 0, 1])
                self.x -= 3
            elif pygame.key.get_pressed()[pygame.K_RIGHT] and self.x < self.width - 40 and not self.touchRight:
                # self.step([1, 0, 0])
                self.x += 3
            for event in pygame.event.get():
                if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]:
                    self.done = True
                    self.close()


    def mouseDebug(self) -> None:
        if self.display is not None:
            x, y = pygame.mouse.get_pos()
            rect = pygame.Rect(x, y, 20, 20)
            if rect.collidelist(self.blocks) != -1:
                pygame.draw.rect(self.display, (255, 0, 0), rect)
            else:
                pygame.draw.rect(self.display, (0, 255, 0), rect)

    def debugMonitor(self) -> None:
        if self.display is not None and self.text is not None:
            self.display.blit(self.text.render("x:{}   y:{}".format(self.x, self.y), True, (0, 0, 0), (255, 255, 255)), [10, 40])
            self.display.blit(self.text.render("x2:{}  y2:{}".format(self.x + 40, self.y + 40), True, (0, 0, 0), (255, 255, 255)), [10, 60])
            self.display.blit(self.text.render("touch ground:{}".format(self.touchGround), True, (0, 0, 0), (255, 255, 255)), [10, 80])
            self.display.blit(self.text.render("touch left:{}".format(self.touchLeft), True, (0, 0, 0), (255, 255, 255)), [10, 100])
            self.display.blit(self.text.render("touch right:{}".format(self.touchRight), True, (0, 0, 0), (255, 255, 255)), [10, 120])
            self.display.blit(self.text.render("touch bottom:{}".format(self.touchBottom), True, (0, 0, 0), (255, 255, 255)), [10, 140])
            self.display.blit(self.text.render("acceleration:{}".format(round(self.acceleration, 2)), True, (0, 0, 0), (255, 255, 255)), [10, 160])
            self.display.blit(self.text.render(f"move up:{self.moveUp}", True, (0, 0, 0), (255, 255, 255)), [10, 180])
            self.display.blit(self.text.render(f"move down:{self.moveDown}", True, (0, 0, 0), (255, 255, 255)), [10, 200])
            self.display.blit(self.text.render(f"animation progress:{self.animationProgress}", True, (0, 0, 0), (255, 255, 255)), [10, 220])

    def debugMonitor2(self) -> None:
        if self.display is not None and self.text is not None:
            self.display.blit(self.text.render(f"nearest star:{round(self.getNearestStar(), 2)}", True, (0, 0, 0), (255, 255, 255)), [10, 40])

            self.display.blit(self.text.render("nearest blocks:", True, (0, 0, 0), (255, 255, 255)), [10, 60])
            for index, block in enumerate(self.getNearestBlocks()):
                self.display.blit(self.text.render(f"{block}", True, (0, 0, 0), (255, 255, 255)), [10, 75 + index * 15])


    def line(self, x1, y1, x2, y2, color) -> None:
        pygame.draw.line(self.display, color, (x1, y1),(x2, y2), width=3)


    def frameMonitor(self) -> None:
        if self.display is not None and self.text is not None:
            self.frames += 1

            if self.currentTime != math.floor(time.time()):
                if self.frames < 60: self.frames = 60
                self.framesMax = str(self.frames)
                self.frames = 0
                self.currentTime = math.floor(time.time())
            self.display.blit(self.text.render(self.framesMax, True, (0, 0, 0), (255, 255, 255)), [10, 10])
