import unittest
from go_game import GoGame

class TestGoGame(unittest.TestCase):

    def test_basics(self):
        game = GoGame(5, 5)
        goban = game.goban
        self.assertEqual(goban.get([0, 0]), 0)

    def test_play_move(self):
        game = GoGame(5, 5)

        turn = 1
        for m in [[0,0], [1,0], [0,1], [1,1], [0,2], [1,2],
                  [0,3], [1,3], [0,4], [1,4]]:
            game.play_move(m, turn)
            print("\n" + game.to_s())
            turn = game.other_color(turn)

        self.assertEqual(game.goban.get([0,0]), 0)

    # def test_ko(self):
    #     board = GoGame(5, 5)

    #     turn = 1
    #     for m in [[0,0], [3,0],
    #               [1,1], [2,1],
    #               [2,0]]:
    #         board.play_move(m, turn)
    #         print("\n" + board.to_s())
    #         turn = board.other_color(turn)

    #     self.assertEqual(board.get([2,0]), 1)
    #     self.assertEqual(True, board.is_legal_move([1,0], turn))

    #     board.play_move([1,0], turn)
    #     print("\n" + board.to_s())
    #     turn = board.other_color(turn)
    #     self.assertEqual(False, board.is_legal_move([2,0], turn))

    #     # fake ko threat
    #     for m in [[3,4], [4,4]]:
    #         board.play_move(m, turn)
    #         print("\n" + board.to_s())
    #         turn = board.other_color(turn)

    #     self.assertEqual(True, board.is_legal_move([2,0], turn))

    # def test_suicide(self):
    #     board = GoGame(5, 5)
    #     for m in [[2,0], [2,1], [1,2], [0,3]]:
    #         board.play_move(m, 1)
    #     for m in [[0,0], [0,1], [0,2], [1,1]]:
    #         board.play_move(m, 2)
    #     print("\n" + board.to_s())
    #     self.assertEqual(False, board.is_legal_move([1,0], 2))

if __name__ == '__main__':
    unittest.main()
