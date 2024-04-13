from array import array
import sys

class Goban:
    """
    A class representing a go board and stones.

    Immutable.

    Methods include setting and getting the state as well as checking
    for dead strings.
    """

    def __init__(self, width, height, boardstate = None):
        self.width = width
        self.height = height
        if boardstate == None:
            boardstate = array('B', bytes(width*height))
        self.boardstate = boardstate

    def _point2index(self, point):
        x = point[0]
        y = point[1]
        return x + self.width * y

    def move_point(self, p, dir):
        p = p.copy()
        if dir == 0:
            p[0] += 1
        elif dir == 1:
            p[1] += 1
        elif dir == 2:
            p[0] -= 1
        elif dir == 3:
            p[1] -= 1
        if p[0] < 0 or p[0] >= self.width or p[1] < 0 or p[1] >= self.height:
            return None
        return p

    def get(self, point):
        return self.boardstate[self._point2index(point)]

    def set(self, point, color):
        new_boardstate = array('B', self.boardstate)
        new_boardstate[self._point2index(point)] = color
        return Goban(self.width, self.height, new_boardstate)

    def board_char(self, a):
        if a == 2:
            return "o"
        if a == 1:
            return "x"
        return "."

    def to_s(self):
        s = ""
        for y in range(self.height-1,-1,-1):
            row_chars = (self.board_char(self.get([x, y])) for x in range(self.width))
            s += " ".join(row_chars) + "\n"
        return s

    def find_dead_string(self, color, points, points_to_search):
        """
        Searches for a dead string of color *color*.

        * *points*: the points found in the string already
        * *points_to_search*: points whose neighbors still need to be
          searched
        """

        # avoid mutation
        points = points.copy()
        points_to_search = points_to_search.copy()

        while len(points_to_search):
            p = points_to_search.pop()
            for dir in range(4):
                new_p = self.move_point(p, dir)
                if None == new_p:
                    continue
                state = self.get(new_p)

                # Skip points already in the string.
                # Important to do that here since for testing captures we
                # insert the attacking stone.
                if points.count(new_p):
                    continue

                if 0 == state:
                    return None
                if color == state:
                    points.append(new_p)
                    points_to_search.append(new_p)

        return points
