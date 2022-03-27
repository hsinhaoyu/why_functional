from typing import List, Iterator, Callable, Optional
from functools import reduce
from random import shuffle

from lazy_utils import Node
import lazy_utils
import game
from game import State

### gameplay options
use_player_token = True
shuffle_moves = False
max_depth = 5

posinf = 100000
neginf = -1 * posinf

num_pos = 9
line_idx = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8],
            [0, 4, 8], [2, 4, 6]]

# Cell is a type alias for representing the state of a cell in a board
Cell = Optional[int]
# Board is a type alias for representing board configurations
Board = List[Cell]


def init_board() -> Board:
    """Creat an empty board.
    An unoccupied position is represented by None"""
    board: List[Optional[int]] = [None for i in range(num_pos)]
    return board


def board_line(line_idx: List[int], board: Board) -> List[Cell]:
    """Return a line (one of line_idx) of a board"""
    return [board[i] for i in line_idx]


def board_lines(board: Board) -> List[List[Cell]]:
    """Return all the lines in a board"""
    return list(map(lambda idx: board_line(idx, board), line_idx))


def won(board: Board, player: int) -> bool:
    """Has player won?"""
    assert player in [0, 1]
    lines = board_lines(board)

    if any(map(lambda l: l.count(player) == 3, lines)):
        return True
    else:
        return False


def who_plays(board: Board) -> int:
    """Which player is playing the next move?"""
    return board.count(0) - board.count(1)


def make_move(board: Board, move: int, current_player: int) -> Board:
    """Apply a move (0-8) to a board for a player.
    Return a new board.
    """
    new_board = board.copy()
    assert new_board[move] is None
    assert current_player in [0, 1]

    new_board[move] = current_player

    return new_board


def moves(board: Board) -> Optional[Iterator[Board]]:
    """Returns an iterator of boards for all legal next moves."""
    next_player = who_plays(board)
    other_player = (next_player + 1) % 2

    if won(board, other_player):
        # There is no legal move if the game is already won
        return None
    else:
        candidate_moves = [i for i in range(num_pos) if board[i] is None]

        if shuffle_moves:
            shuffle(candidate_moves)

        if len(candidate_moves) == 0:
            return None
        else:
            return map(lambda i: make_move(board, i, next_player),
                       candidate_moves)


gametree: Callable[[Board], Node] = game.gametree(moves)


def prune(tree: Node) -> Node:
    return lazy_utils.prune(max_depth, tree)


### Heuristic evaluation of board configurations
def is_good_line(n: int, player: int, line: List[Cell]) -> bool:
    """A typical way to evaluate if a line is good"""

    assert n in [1, 2]
    assert player in [0, 1]

    v1 = line.count(player) == n
    v2 = line.count(None) == 3 - n
    return v1 and v2


def count_good_lines(n: int, player: int, lines: List[List[Cell]]) -> int:
    """How many good lines?"""

    assert n in [1, 2]
    assert player in [0, 1]

    zz = list(map(lambda l: is_good_line(n, player, l), lines))
    return zz.count(True)


def static_eval_0(board: Board) -> int:
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


def static_eval(player: int) -> Callable[[Board], int]:
    """Static board value for player i"""
    assert player in [0, 1]

    def static_eval_(board):
        v = static_eval_0(board)
        if player == 0:
            return v
        else:
            return -1 * v

    return static_eval_


# given a player, returns a tree evlauation function
def evaluate0(player: int) -> Callable[[Board], int]:
    """Evaluate tic-tac-toe tree for player i (version 1)"""
    return game.evaluate0(gametree, static_eval(player), prune)


def static_eval_state(i: int) -> Callable[[Board], State]:
    """Static board state for player i"""
    assert i in [0, 1]
    score_func = static_eval(i)

    def static_eval_(board):
        return State(board, score_func(board))

    return static_eval_


# given a player, returns a tree evlauation function
def evaluate1(player: int) -> Callable[[Board], State]:
    """Evaluate tic-tac-toe tree for player i (version 1)"""
    return game.evaluate1(gametree, static_eval_state(player), prune)


def player_token(i: int) -> str:
    assert i in [0, 1]
    if use_player_token:
        return "X" if i == 0 else "O"
    else:
        return "0" if i == 0 else "1"


def display_board(board: Board, coordinates=False) -> None:
    """Display a board"""
    def row(lst):
        return reduce(lambda a, b: a + " " + b, lst, "")

    d = {None: '.', 1: player_token(1), 0: player_token(0)}

    zz = list(map(lambda i: d[i], board))
    zz = [zz[i:i + 3] for i in range(0, 9, 3)]
    zz = list(map(row, zz))

    if coordinates:

        def d_(i):
            if board[i] is None:
                return str(i)
            else:
                return "."

        zz2 = [d_(i) for i in range(9)]
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


def human_next_move(board: Board) -> Optional[Board]:
    """Display current board, ask player to make the next move.
    Return a board after the player's move.
    """
    display_board(board, coordinates=True)
    legal_moves = [i for i in range(num_pos) if board[i] is None]
    if legal_moves == []:
        return None
    else:
        player = who_plays(board)

        ok = False
        while not ok:
            m = input(f"player {player_token(player)} move?")
            try:
                i = int(m)
                if i in legal_moves:
                    ok = True
            except ValueError:
                pass

        return make_move(board, i, player)


def computer_next_move(
        board: Board, eval_func: Callable[[int],
                                          Callable[[Board],
                                                   State]]) -> Optional[Board]:
    player = who_plays(board)
    computer_move_function = eval_func(player)
    # computer_move_function is a State
    return computer_move_function(board).board


def player_next_move(board: Board,
                     player_settings={
                         0: 'human',
                         1: 'computer'
                     },
                     eval_func=evaluate1) -> Optional[Board]:
    player = who_plays(board)
    if player_settings[player] == 'human':
        return human_next_move(board)
    else:
        return computer_next_move(board, eval_func)


def play(
        player_settings={
            0: 'human',
            1: 'computer'
        },
        eval_func=evaluate1) -> None:
    b = init_board()

    finished = False
    while not finished:
        b = player_next_move(b, player_settings, eval_func)
        player = (who_plays(b) + 1) % 2
        print()
        print(f"{player_token(player)} played:")
        display_board(b)
        print()

        assert b is not None
        if won(b, player):
            print(f"{player_token(player)} won!")
            finished = True
        elif len([i for i in range(num_pos) if b[i] is None]) == 0:
            print("Draw!")
            finished = True
