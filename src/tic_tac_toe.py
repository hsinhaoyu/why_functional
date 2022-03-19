from typing import List, Iterator, Union, Callable
from functools import reduce
from lazy_utils import maptree
import lazy_utils
import game
#from game import gametree, maximize, evaluate1, ai_next_move
### searching
max_depth = 5

### board configuration and geometry
posinf = 100000
neginf = -1 * posinf

num_pos = 9
line_idx = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8],
            [0, 4, 8], [2, 4, 6]]


def init_board() -> List:
    """Creat an empty board.
    An unoccupied position is represented by None"""
    board = [None for i in range(num_pos)]
    return board


def board_line(line_idx: List, board: List) -> List:
    """Return a line (one of line_idx) of a board"""
    return [board[i] for i in line_idx]


def board_lines(board: List) -> List:
    """Return all the lines in a board"""
    return list(map(lambda idx: board_line(idx, board), line_idx))


def won(board: List, player: int) -> bool:
    """Has player won?"""
    assert player in [0, 1]
    lines = board_lines(board)

    if any(map(lambda l: l.count(player) == 3, lines)):
        return True
    else:
        return False


### Moves
def make_move(board: List, move: int, current_player: int) -> List:
    """Apply a move (0-8) to a board for a player.
    Return a new board.
    """
    new_board = board.copy()
    assert new_board[move] is None
    assert current_player in [0, 1]

    new_board[move] = current_player

    return new_board


def who_plays(board: List) -> int:
    return board.count(0) - board.count(1)


def moves(board: List) -> Union[Iterator, None]:
    """Returns an iterator of boards for all legal next moves.
    Player 0 (X) always makes the first move in a game.
    """
    next_player = who_plays(board)
    other_player = (next_player + 1) % 2

    if won(board, other_player):
        # There is no legal move if the game is already won
        return None
    else:
        candidate_moves = [i for i in range(num_pos) if board[i] is None]
        if len(candidate_moves) == 0:
            return None
        else:
            return map(lambda i: make_move(board, i, next_player),
                       candidate_moves)


### game I/O
def display_board(board: List, coordinates=False, displayXO=False) -> None:
    """Display a board"""

    def row(lst):
        return reduce(lambda a, b: a + " " + b, lst, "")

    if displayXO:
        d = {None: '.', 1: 'O', 0: 'X'}
    else:
        d = {None: '.', 1: '1', 0: '0'}

    zz = list(map(lambda i: d[i], board))
    zz = [zz[i:i + 3] for i in range(0, 9, 3)]
    zz = list(map(row, zz))

    if coordinates:

        def d(i):
            if board[i] is None:
                return str(i)
            else:
                return "."

        zz2 = [d(i) for i in range(9)]
        zz2 = [zz2[i:i + 3] for i in range(0, 9, 3)]
        zz2 = list(map(row, zz2))

    res = ""
    if coordinates:
        for i in range(3):
            res = res + zz[i] + "\t\t" + zz2[i] + "\n"
    else:
        for i in range(3):
            res = res + zz[i] + "\n"

    print(res[:-1])


def player_input(board: List) -> List:
    """Display current board, ask player to make the next move.
    Return a board after the player's move.
    """
    display_board(board, coordinates=True)
    legal_moves = [i for i in range(9) if board[i] is None]
    ok = False
    while not ok:
        m = input("move?")
        try:
            i = int(m)
            if i in legal_moves:
                ok = True
        except ValueError:
            pass

    # the human player is always player 0
    return make_move(board, i, 0)


### Heuristic evaluation of board configurations
def is_good_line(n: int, player: int, line: List) -> bool:
    """A typical way to evaluate if a line is good"""

    assert n in [1, 2]
    assert player in [0, 1]

    v1 = line.count(player) == n
    v2 = line.count(None) == 3 - n
    return v1 and v2


def count_good_lines(n: int, player: int, lines: List) -> int:
    """How many good lines?"""

    assert n in [1, 2]
    assert player in [0, 1]

    zz = list(map(lambda l: is_good_line(n, player, l), lines))
    return zz.count(True)


def static_eval_0(board: List) -> int:
    """Static board value for player 0
    >0: player 0 is doing better
    <0: player 1 is doing better
    """
    lines = board_lines(board)

    if any(map(lambda l: l.count(0) == 3, lines)):
        val = posinf
    elif any(map(lambda l: l.count(1) == 3, lines)):
        val = neginf
    else:
        x2 = count_good_lines(2, 0, lines)
        x1 = count_good_lines(1, 0, lines)

        o2 = count_good_lines(2, 1, lines)
        o1 = count_good_lines(1, 1, lines)

        val = 3 * x2 + x1 - (3 * o2 + o1)
    return val


def static_eval(i: int) -> Callable[[List], int]:
    """Static board value for player i"""
    assert i in [0, 1]

    def static_eval_(board):
        v = static_eval_0(board)
        if i == 0:
            return v
        else:
            return -1 * v

    return static_eval_


gametree = game.gametree(moves)


def prune(tree):
    return lazy_utils.prune(max_depth, tree)


evaluate1 = game.evaluate1(gametree, static_eval(1), prune)


def play(tree_eval_func):
    b = init_board()

    finished = False
    while not finished:
        b = player_input(b)
        print()
        print("you played:")
        display_board(b)
        print()

        if won(b, 0):
            print("You've won!")
            finished = True
        else:
            b = ai_next_move(b, moves, tree_eval_func)
            if b is None:
                print("Draw!")
                finished = True
            elif won(b, 1):
                print("computer played: ")
                display_board(b)
                print("You've lost!")
                finished = True
            else:
                print("computer played:")


def play1():

    def eval_(board):
        return evaluate1(board, moves, static_eval(1))

    play(eval_)
