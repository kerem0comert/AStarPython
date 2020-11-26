from Point import Point

class Candidate(Point):
    def __init__(self, x, y, g, h):
        super().__init__(x, y)
        self.g = g
        self.h = h
    
    def __eq__(self, c): return self.__dict__ == c.__dict__