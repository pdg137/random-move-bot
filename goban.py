from array import array

class Goban:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.boardstate = array('B', bytes(width*height))

    def state(self, point):
        return self.boardstate[self.point2index(point)]

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

    def board_char(self, a):
        if a == 2:
            return "o"
        if a == 1:
            return "x"
        return "."

    def to_s(self):
        s = ""
        for y in range(self.height):
            row_chars = (self.board_char(self.state([x, y])) for x in range(self.width))
            s += " ".join(row_chars) + "\n"
        return s

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

    def find_dead_string(self, color, points, points_to_search):
        # avoid mutation
        points = points.copy()
        points_to_search = points_to_search.copy()

        while len(points_to_search):
            p = points_to_search.pop()
            for dir in range(4):
                new_p = self.move_point(p, dir)
                if None == new_p:
                    continue
                state = self.state(new_p)
                if 0 == state:
                    return None
                if color == state:
                    if 0 == points.count(new_p):
                        points.append(new_p)
                        points_to_search.append(new_p)

        return points

    def is_legal_move(self, point, color):
        # no suicide
        if self.find_dead_string(color, [point], [point]):
            return False

        # TODO: repetition

        return True

    def other_color(self, color):
        if color == 1:
            return 2
        elif color == 2:
            return 1
        return 0

    def play_move(self, point, color):
        if not self.is_legal_move(point, color):
            raise ValueError(point)
        self.set(point, color)
        for dir in range(4):
            new_p = self.move_point(point, dir)
            if None == new_p:
                continue

            string = self.find_dead_string(self.other_color(color), [new_p], [new_p])
            if string:
                # dead!
                for p in string:
                    self.set(p, 0)
