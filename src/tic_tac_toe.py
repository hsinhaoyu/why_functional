from typing import Tuple, List, Union, Iterator
from functools import reduce

num_pos = 9


def mk_state(board, player, move):
    return (board, player, move)


def decompose_state(state):
    board = state[0]
    last_player = state[1]
    last_move = state[2]
    return (board, last_player, last_move)


def init_state():
    board = [None for i in range(num_pos)]
    last_player = None
    last_move = None
    return mk_state(board, last_player, last_move)


def make_move(board, move: int, current_player: int) -> List:
    new_board = board.copy()
    assert new_board[move] == None

    new_board[move] = current_player

    return mk_state(new_board, current_player, move)


def moves(state) -> Iterator:
    """Returns an iterator of game states of all legal next moves"""
    (board, last_player, last_move) = decompose_state(state)
    if last_player is None:
        next_player = 0
    else:
        next_player = (last_player + 1) % 2

    candidate_moves = [i for i in range(num_pos) if board[i] is None]
    return map(lambda i: make_move(board, i, next_player), candidate_moves)


def display_board(board):

    def row(lst):
        return reduce(lambda a, b: a + b, lst, "")

    d = {None: '.', 0: 'O', 1: 'X'}
    zz = list(map(lambda i: d[i], board))
    zz = [zz[i:i + 3] for i in range(0, 9, 3)]
    zz = map(row, zz)
    zz = reduce(lambda a, b: a + "\n" + b, zz, "")
    print(zz)
