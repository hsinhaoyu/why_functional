from functools import reduce
from typing import Callable, List, Iterator, Tuple, Optional, Union
from lazy_utils import reptree, maptree, Node
import operator

# Board is a type alias for representing a board configuration.
# In this example,  it's just a list
Board = List


def max_assoc(itr: Iterator[Tuple[Board, int]]) -> Board:
    """Return the board with the highest score."""

    def max_f(new_item: Tuple[Board, int], old_item: Tuple[Board, int]):
        return new_item if new_item[1] > old_item[1] else old_item

    first_item = next(itr)
    return reduce(max_f, itr, first_item)[0]


def gametree(
    moves: Callable[[Board], Optional[Iterator[Board]]]
) -> Callable[[Board], Node]:
    """Return a func that builds a gametree from an initial board.
    moves is a function that returns all legal moves given a board.
    """

    def gametree_(board: Board) -> Node:
        return reptree(moves, board)

    return gametree_


def maximize1(gametree: Node) -> int:
    """The max step of Minimax"""
    (score, subtrees) = gametree

    if subtrees is None:
        s = score
    else:
        s = max(map(minimize1, subtrees))
    return s


def minimize1(gametree: Node) -> int:
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


def evaluate1(gametree_: Callable[[Board],
                                  Node], static_eval_: Callable[[Board], int],
              prune_: Callable[[Node], Node]) -> Callable[[Board], int]:
    """Return a tree evaluation function"""

    def evaluate_(board: Board) -> int:
        return minimize1(maptree(static_eval_, prune_(gametree_(board))))

    return evaluate_


def max_next_move(
    gametree_func: Callable[[Board], Node],
    tree_eval_func: Callable[[Board],
                             int]) -> Callable[[Board], Optional[Board]]:
    """Return a function to make the next move."""

    def max_next_move_(board: Board) -> Optional[Board]:
        # return a board or None
        (_, subtree) = gametree_func(board)
        if subtree is None:
            return None
        else:
            subtrees_evaluated = map(
                lambda next_move: (next_move[0], tree_eval_func(next_move[0])),
                subtree)
            return max_assoc(subtrees_evaluated)

    return max_next_move_


def mapmin(seqs: Iterator[Iterator]) -> Iterator:
    """Like map(min, seqs)
    But skip those that don't matter for max.
    The sequence increases monotonically
    """
    try:
        seq = next(seqs)
        mn = min(seq)
        yield mn
        for i in omit_max(mn, seqs):
            yield i
    except StopIteration:
        pass


def mapmax(seqs: Iterator[Iterator]) -> Iterator:
    """Like map(max, seqs)
    But skip those that don't matter for min
    The sequence decreases monotonically
    """
    try:
        seq = next(seqs)
        mx = max(seq)
        yield mx
        for i in omit_min(mx, seqs):
            yield i
    except StopIteration:
        pass


def mk_omit(skip_func: Callable) -> Callable:
    """The skip function is either minleq or maxgeq"""

    def omit_(
            pot: int, seqs: Optional[Iterator[Iterator[int]]]
    ) -> Iterator[Optional[int]]:
        """Given an iterator of iterators, call skip_func.
        If the returned value is true, skip it. Otherwise, yield the value
        """
        for seq in seqs:
            m = skip_func(seq, pot)
            if m is True:
                for i in omit_(pot, seqs):
                    yield i
            else:
                yield m
                for i in omit_(m, seqs):
                    yield i

    return omit_


def mk_ab_seq(comp: Callable, op: Callable) -> Callable:
    """Given a comparison function comp and an operator op, return a function."""

    def ab_seq(seq: Optional[Iterator],
               pot: int) -> Optional[Union[int, bool]]:
        """Efficient min/max of an iterator, given potential max/min"""

        def ab_seq_(seq, current_val):
            try:
                i = next(seq)
                if current_val is None:
                    current_val = i

                if comp(i, pot):
                    # if smaller, returns true immediately
                    return True
                else:
                    return ab_seq_(seq, op(i, current_val))
            except StopIteration:
                if current_val is None:
                    return pot
                else:
                    return current_val

        if seq is None:
            return pot
        else:
            return ab_seq_(seq, None)

    return ab_seq


minleq = mk_ab_seq(operator.le, min)
minleq.__doc__ = """
Return min of seq if it's > potential max.
Else return True"""

maxgeq = mk_ab_seq(operator.ge, max)
maxgeq.__doc__ = """
Return max of seq if it's < potential min.
Else return True"""

omit_max = mk_omit(minleq)
omit_max.__doc__ = """
Given an initial potential max, return the min of subsequences.
Skip those that don't matter. Sequence increases.
"""

omit_min = mk_omit(maxgeq)
omit_max.__doc__ = """
Given an initial potental min, return the max of subsequences.
Skip those that don't matter. Sequence decreases.
"""
