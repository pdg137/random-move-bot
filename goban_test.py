import unittest
from goban import Goban

class TestGoban(unittest.TestCase):

    def test_basics(self):
        board = Goban(5, 5)
        self.assertEqual(board.state(0, 0), 0)
        board.set([0, 0], 1)
        self.assertEqual(board.state(0, 0), 1)

if __name__ == '__main__':
    unittest.main()
