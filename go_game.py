from goban import Goban

class GoGame:
    """
    A class representing a game of go.  Includes board state, history,
    and player to move. Methods include checking legality of moves and
    making the moves.
    """

    def __init__(self, width, height):
        self.goban = Goban(width, height)
        self.previous_positions = []
        self.record_position()

    def record_position(self):
        self.previous_positions.append(self.goban)

    def previous_position_exists(self, test_goban):
        return self.previous_positions.count(test_goban)

    def __repr__(self):
        return str(self.goban)

    def is_legal_move(self, point, color):
        if 0 != self.goban.get(point):
            # occupied
            return False

        # no repetition
        tmp_goban = self.apply_move_to_board(point, color)
        if self.previous_position_exists(tmp_goban):
            return False
        if 0 == tmp_goban.get(point):
            # suicide
            return False

        return True

    def other_color(self, color):
        if color == 1:
            return 2
        elif color == 2:
            return 1
        return 0

    def apply_move_to_board(self, point, color):
        new_goban = self.goban.set(point, color)
        for dir in range(4):
            new_p = new_goban.move_point(point, dir)
            if None == new_p:
                continue

            # can't be dead if it's empty
            if 0 == new_goban.get(new_p):
                continue

            # handle suicide later
            if color == new_goban.get(new_p):
                continue

            string = new_goban.find_dead_string(self.other_color(color), [new_p], [new_p])
            if string:
                # dead!
                for p in string:
                    new_goban = new_goban.set(p, 0)

        # checking suicide
        string = new_goban.find_dead_string(color, [point], [point])
        if string:
            # dead!
            for p in string:
                new_goban = new_goban.set(p, 0)

        return new_goban

    def play_move(self, point, color):
        if not self.is_legal_move(point, color):
            raise ValueError([str(self.goban), point])

        self.goban = self.apply_move_to_board(point, color)

        self.record_position()
