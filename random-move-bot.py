import random
from gtp_bot import GtpBot

def genmove(game, color):
    col = None
    row = None
    for i in range(1000):
        col = random.randrange(game.goban.width)
        row = random.randrange(game.goban.height)
        if bot.game.is_legal_move([col, row], color):
            break
    return [col, row]

def place_free_handicap(game, handicap):
    moves = []
    for i in range(handicap):
        for j in range(1000):
            move = genmove(game, 1)
            if 0 == moves.count(move):
                break
        moves.append(move)
    return moves

bot = GtpBot(place_free_handicap, genmove)

bot.run()
