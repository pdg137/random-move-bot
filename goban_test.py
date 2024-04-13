import unittest
from goban import Goban

class TestGoGame(unittest.TestCase):

    def test_basics(self):
        board = Goban(5,5)
        self.assertEqual(board.get([0, 0]), 0)
        board2 = board.set([0, 0], 1)
        self.assertEqual(board2.get([0, 0]), 1)
        board3 = board.set([0, 0], 1)
        self.assertEqual(board2, board3)
        print(board.to_s())

    def test_find_dead_string_simple(self):
        board = Goban(5, 5).set([0, 0], 1)

        result = board.find_dead_string(1, [[0,0]], [[0,0]])
        self.assertEqual(None, result)

        board = board.set([1, 0], 2)
        board = board.set([0, 1], 2)
        result = board.find_dead_string(1, [[0,0]], [[0,0]])
        self.assertEqual([[0, 0]], result)

    def test_find_dead_string_larger(self):
        board = Goban(5, 5).set([0, 0], 1).set([1, 0], 1).set([0, 1], 2)
        result = board.find_dead_string(1,[[0,0]], [[0,0]])
        self.assertEqual(None, result)
        print("\n" + board.to_s())

        board = board.set([1, 1], 2).set([2, 0], 2)
        result = board.find_dead_string(1,[[0,0]], [[0,0]])
        self.assertEqual([[0,0], [1,0]], result)
        print("\n", board.to_s())

    def test_find_dead_string_larger2(self):
        board = Goban(5, 5)

        for p in [[2,2],[3,2],[1,2],[2,1],[2,3]]:
            board = board.set(p, 1)
        for p in [[0,2],[1,1],[2,0],[4,2],[3,3],[2,4],[1,3]]:
            board = board.set(p, 2)
        result = board.find_dead_string(1,[[2,2]], [[2,2]])
        self.assertEqual(None, result)
        print("\n" + board.to_s())

        board = board.set([3,1], 2)
        result = board.find_dead_string(1,[[2,2]], [[2,2]])
        self.assertEqual([[2,2],[3,2],[1,2],[2,1],[2,3]].sort(), result.sort())
        print("\n" + board.to_s())

if __name__ == '__main__':
    unittest.main()
