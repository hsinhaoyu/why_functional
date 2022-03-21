from functools import reduce
from typing import Callable, List, Union, Iterator, Tuple
from lazy_utils import reptree, maptree, prune


def gametree(
        moves: Callable[[List], Union[Iterator,
                                      None]]) -> Callable[[List], Tuple]:
    """Return a func that builds a gametree from an initial board.
    moves is a function that returns all legal moves given a board.
    """

    def gametree_(board):
        return reptree(moves, board)

    return gametree_


def maximize1(gametree: Tuple) -> int:
    """The max step of Minimax"""
    (score, subtrees) = gametree

    if subtrees is None:
        s = score
    else:
        s = max(map(minimize1, subtrees))
    return s


def minimize1(gametree: Tuple) -> int:
    """The min step of Minimax.
    A node in gametree is ((board, score), subtrees)
    Returns (board, score) with the minimal score
    """
    (score, subtrees) = gametree

    if subtrees is None:
        s = score
    else:
        s = min(map(maximize1, subtrees))
    return s


def evaluate1(gametree_: Callable, eval_: Callable,
              prune_: Callable) -> Callable:

    def evaluate_(board: Tuple) -> int:
        return minimize1(maptree(eval_, prune_(gametree_(board))))

    return evaluate_


def max_assoc(itr):
    """ Return the board with the highest score.
    itr is (board1, score1), (board2, score2)...
    """

    def max_f(new_item, old_item):
        return new_item if new_item[1] > old_item[1] else old_item

    first_item = next(itr)
    return reduce(max_f, itr, first_item)[0]


def max_next_move(gametree_func: Callable,
                  tree_eval_func: Callable) -> Callable:
    """Return a function to make the next move."""

    def max_next_move_(board: List) -> Union[List, None]:
        # return a board or None
        (_, subtree) = gametree_func(board)
        subtrees_evaluated = map(
            lambda next_move: (next_move[0], tree_eval_func(next_move[0])),
            subtree)
        return max_assoc(subtrees_evaluated)

    return max_next_move_
