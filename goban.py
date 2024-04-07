from array import array

class Goban:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.boardstate = array('B', bytes(width*height))
        self.previous_positions = []
        self.record_position()

    def record_position(self):
        self.previous_positions.append(array('B', self.boardstate))

    def previous_position_exists(self, test_boardstate):
        return self.previous_positions.count(test_boardstate)

    def get(self, point, boardstate = None):
        if None == boardstate:
            boardstate = self.boardstate
        return boardstate[self.point2index(point)]

    def point2index(self, point):
        x = point[0]
        y = point[1]
        return x + self.width * y

#    def index2point(self, index):
#        x = index % self.width
#        y = index // self.width
#        return [x, y]

    def set(self, point, color, boardstate = None):
        if None == boardstate:
            boardstate = self.boardstate
        boardstate[self.point2index(point)] = color

    def board_char(self, a):
        if a == 2:
            return "o"
        if a == 1:
            return "x"
        return "."

    def to_s(self):
        s = ""
        for y in range(self.height):
            row_chars = (self.board_char(self.get([x, y])) for x in range(self.width))
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

    def find_dead_string(self, color, points, points_to_search, boardstate = None):
        if None == boardstate:
            boardstate = self.boardstate

        # avoid mutation
        points = points.copy()
        points_to_search = points_to_search.copy()

        while len(points_to_search):
            p = points_to_search.pop()
            for dir in range(4):
                new_p = self.move_point(p, dir)
                if None == new_p:
                    continue
                state = self.get(new_p, boardstate)

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

    def is_legal_move(self, point, color):
        # no repetition
        tmp_boardstate = array('B', self.boardstate)
        self.apply_move_to_board(point, color, tmp_boardstate)
        if self.previous_position_exists(tmp_boardstate):
            return False

        for dir in range(4):
            new_p = self.move_point(point, dir)
            if None == new_p:
                continue

            string = self.find_dead_string(self.other_color(color), [point, new_p], [new_p])
            if string:
                # if you kill a group, it's always legal
                return True

        # no suicide
        if self.find_dead_string(color, [point], [point]):
            return False

        return True

    def other_color(self, color):
        if color == 1:
            return 2
        elif color == 2:
            return 1
        return 0

    def apply_move_to_board(self, point, color, boardstate):
        self.set(point, color, boardstate)
        for dir in range(4):
            new_p = self.move_point(point, dir)
            if None == new_p:
                continue

            # assume it's not suicide, nothing to check
            if color == new_p:
                continue

            string = self.find_dead_string(self.other_color(color), [new_p], [new_p], boardstate)
            if string:
                # dead!
                for p in string:
                    self.set(p, 0, boardstate)

    def play_move(self, point, color):
        if not self.is_legal_move(point, color):
            raise ValueError(point)

        self.apply_move_to_board(point, color, self.boardstate)

        self.record_position()
