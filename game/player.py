from game.map import Square


class Player:
    def __init__(self, position=Square(0, 0), elevation=0):
        self.position = position
        self.elevation = elevation

    def climb(self):
        self.elevation += 1
