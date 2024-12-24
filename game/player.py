from game.map import Square


class Player:
    def __init__(self, position=Square(0, 0)):
        self.elevation = 0
        self.position = position

    def climb(self):
        self.elevation += 1
