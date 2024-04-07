from array import array

class Goban:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.boardstate = array('B', bytes(width*height))

    def state(self, x, y):
        return self.boardstate[self.point2index([x, y])]

    def point2index(self, point):
        x = point[0]
        y = point[1]
        return x + self.width * y

#    def index2point(self, index):
#        x = index % self.width
#        y = index // self.width
#        return [x, y]

    def set(self, point, color):
        self.boardstate[self.point2index(point)] = color
