
class Scoreboard:

    def __init__(self) -> None:
        self.score: int = 0
    
    def renderScore(self) -> None:
        self.display.blit(self.text.render(f"Score: {self.score}", True, (0, 0, 0), (255, 255, 255)), [self.width - 90, 15])

    def addScore(self) -> None:
        self.score += 1

    def resetScore(self) -> None:
        self.score = 0
