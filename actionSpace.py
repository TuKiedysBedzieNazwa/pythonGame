import random

class actionSpace():
    def __init__(self) -> None:
        self.left = [1, 0, 0]
        self.up = [0, 1, 0]
        self.right = [0, 0, 1]

    def sample(self):
        return random.choice([self.left, self.up, self.right])
