from Point import Point

class Node(Point):
    def __init__(self, name, x, y):
        super().__init__(x, y)
        self.name = name

