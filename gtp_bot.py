import sys
from go_game import GoGame

def _debug(str):
    sys.stderr.write(str)
    sys.stderr.write("\n")

class GtpBot:
    """
    Implements the GTP protocol and tracks the ongoing game in a
    GoGame object.
    """

    def __init__(self, place_free_handicap, genmove):
        self.game = None
        self.komi = 0
        self.handicap = 0
        self.place_free_handicap = place_free_handicap
        self.genmove = genmove

    def _debug_board(self):
        sys.stderr.write(self.game.to_s())

    def _parsemove(self, move):
        if None == move:
            return None
        row = int(move[1:])-1
        if move[0] > "i": # skip i
            col = ord(move[0]) - ord("a") - 1
        else:
            col = ord(move[0]) - ord("a")
        return [col, row]

    def _format_move(self, col, row):
        if col == None:
            return "PASS"
        r = str(row + 1)
        if col >= ord("i") - ord("a"):
            c = chr(ord("a") + col + 1)
        else:
            c = chr(ord("a") + col)
        return c + r

    def _play_moves(self, color, moves):
        move_string = " ".join(self._format_move(m[0], m[1]) for m in moves)
        print(f"= {move_string}\n")
        _debug(f"playing {move_string} as {color}")
        for m in moves:
            self.game.play_move(m, color)

    def run(self):
        while True:
            line = input().strip().split(" ")
            cmd = line[0]
            args = line[1:]
            self._process_command(cmd, args)

    def _process_command(self, cmd, args):
        sys.stderr.write(f"BOT RECEIVED: {cmd} {args}\n")

        match cmd:
            case "list_commands":
                print("""= aa_confirm_safety
boardsize
clear_board
genmove
komi
place_free_handicap
play
set_free_handicap
""")
            case "boardsize":
                width = int(args[0])
                if len(args) > 1:
                    height = int(args[1])
                else:
                    height = width
                self.game = GoGame(width, height)

                print("= \n\n")

            case "clear_board":
                self.game = GoGame(self.game.goban.width, self.game.goban.height)
                self.handicap = 0
                print("= \n")
            case "komi":
                self.komi = float(args[0])
                print("= \n")
            case "set_free_handicap":
                for move in args:
                    (col, row) = self._parsemove(move)
                    _debug(f"playing {move} = [{col}, {row}] as 1")
                    if col >= self.game.goban.width or row >= self.game.goban.height:
                        _debug(f"WARNING: illegal handicap move {move}")
                        continue
                    if self.game.goban.get([col, row]) != 0:
                        _debug(f"WARNING: duplicate handicap move {move}")
                        continue
                    self.game.play_move([col, row], 1)
                    self.handicap += 1
                print("= \n")
            case "place_free_handicap":
                self.handicap = int(args[0])
                moves = self.place_free_handicap(self.game, self.handicap)
                self._play_moves(1, moves)
            case "play":
                if args[0] == "white":
                    color = 2
                else:
                    color = 1
                if args[1] != "pass":
                    (col, row) = self._parsemove(args[1])
                    self.game.play_move([col, row], color)
                print("= \n")
            case "genmove":
                if args[0] == "white":
                    color = 2
                else:
                    color = 1
                move = self.genmove(self.game, color)
                self._play_moves(color, [move])
            case "quit":
                quit()
            case _:
                _debug("UNKNOWN COMMAND")

        if self.game:
            nl = "\n"
            self._debug_board()
