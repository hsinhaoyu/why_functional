from typing import Tuple, List, Union, Iterator
from functools import reduce
from lazy_utils import mk_tree, decompose_tree

num_pos = 9


def init_board():
    board = [None for i in range(num_pos)]
    return board


def make_move(board, move: int, current_player: int) -> List:
    new_board = board.copy()
    assert new_board[move] == None

    new_board[move] = current_player

    return new_board


def moves(board) -> Iterator:
    """Returns an iterator of all legal next moves.
    Player 0 (X) makes the first move in a game.
    """
    next_player = board.count(0) - board.count(1)

    candidate_moves = [i for i in range(num_pos) if board[i] is None]
    return map(lambda i: make_move(board, i, next_player), candidate_moves)


def display_board(board, coordinates=False):

    def row(lst):
        return reduce(lambda a, b: a + b, lst, "")

    d = {None: '.', 1: 'O', 0: 'X'}
    zz = list(map(lambda i: d[i], board))
    zz = [zz[i:i + 3] for i in range(0, 9, 3)]
    zz = list(map(row, zz))

    if coordinates:

        def d(i):
            if board[i] is None:
                return str(i)
            else:
                return " "

        zz2 = [d(i) for i in range(9)]
        zz2 = [zz2[i:i + 3] for i in range(0, 9, 3)]
        zz2 = list(map(row, zz2))

    res = ""
    if coordinates:
        for i in range(3):
            res = res + zz[i] + "\t" + zz2[i] + "\n"
    else:
        for i in range(3):
            res = res + zz[i] + "\n"

    print(res)


def player_input(board):
    display_board(board, coordinates=True)
    legal_moves = [i for i in range(9) if board[i] is None]
    ok = False
    while not ok:
        m = input("move?")
        try:
            i = int(m)
            if i in legal_moves:
                ok = True
        except:
            pass

    # the human player is always player 0
    return make_move(board, i, 0)


line_idx = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8],
            [0, 4, 8], [2, 4, 6]]


def board_line(line_idx, board):
    return [board[i] for i in line_idx]


def board_lines(board):
    return list(map(lambda idx: board_line(idx, board), line_idx))


def is_good_line(n, player, line):
    v1 = line.count(player) == n
    v2 = line.count(None) == 3 - n
    return v1 and v2


def count_good_lines(n, player, lines):
    zz = list(map(lambda l: is_good_line(n, player, l), lines))
    return zz.count(True)


def player0_wins(board):
    lines = board_lines(board)
    return any(map(lambda l: l.count(0) == 3, lines))


def static_eval(board):
    """Static board value.
    >0: player 0 is doing better
    <0: player 1 is doing better
    """
    lines = board_lines(board)

    if any(map(lambda l: l.count(0) == 3, lines)):
        val = 1000000
    elif any(map(lambda l: l.count(1) == 3, lines)):
        val = -1000000
    else:
        x2 = count_good_lines(2, 0, lines)
        x1 = count_good_lines(1, 0, lines)

        o2 = count_good_lines(2, 1, lines)
        o1 = count_good_lines(1, 1, lines)

        val = 3 * x2 + x1 - (3 * o2 + o1)
    return val
