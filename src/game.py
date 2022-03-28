from functools import reduce
from typing import Callable, List, Iterator, Tuple, Optional, Union
from dataclasses import dataclass
import operator

from lazy_utils import reptree, maptree, Node

# Board is a type alias for representing a board configuration.
# In this example,  it's just a list
Board = List


def gametree(
    moves: Callable[[Board], Optional[Iterator[Board]]]
) -> Callable[[Board], Node]:
    """Return a func that builds a gametree from an initial board.
    moves is a function that returns all legal moves given a board.
    """
    def gametree_(board: Board) -> Node:
        return reptree(moves, board)

    return gametree_


def maximize0(node: Node) -> int:
    """The max step of Minimax"""
    (score, subtrees) = node

    if subtrees is None:
        s = score
    else:
        s = max(map(minimize0, subtrees))
    return s


def minimize0(node: Node) -> int:
    """The min step of Minimax.
    A node in gametree is ((board, score), subtrees)
    Returns (board, score) with the minimal score
    """
    (score, subtrees) = node

    if subtrees is None:
        s = score
    else:
        s = min(map(maximize0, subtrees))
    return s


def evaluate0(gametree_: Callable[[Board],
                                  Node], static_eval_: Callable[[Board], int],
              prune_: Callable[[Node], Node]) -> Callable[[Board], int]:
    """Return a tree evaluation function"""
    def evaluate_(board: Board) -> int:
        return maximize0(maptree(static_eval_, prune_(gametree_(board))))

    return evaluate_


@dataclass
class State:
    board: Board
    score: int

    def __eq__(self, other):
        return self.score == other.score

    def __gt__(self, other):
        return self.score > other.score

    def __ge__(self, other):
        return self.score >= other.score

    def __lt__(self, other):
        return self.score < other.score

    def __le__(self, other):
        return self.score <= other.score


def maximize1_(node: Node) -> Iterator[State]:
    """The max step of Minimax before max"""
    (state, subtrees) = node

    if subtrees is None:
        yield state
    else:
        for s in map_(minimize1, subtrees):
            yield s


def maximize1(node: Node) -> State:
    return max(maximize1_(node))


def minimize1_(node: Node) -> Iterator[State]:
    """The min step of Minimax before min"""
    (state, subtrees) = node

    if subtrees is None:
        yield state
    else:
        for s in map_(maximize1, subtrees):
            yield s


def minimize1(node: Node) -> State:
    return min(minimize1_(node))


def map_(func: Callable[[Node], State],
         subtrees: Iterator[Node]) -> Iterator[State]:
    """Replace the board return from map with boards in subtrees"""
    assert subtrees is not None

    for subtree in subtrees:
        # a subtree is a node
        (state0, _) = subtree
        state1 = func(subtree)
        yield State(state0.board, state1.score)


def evaluate1(gametree_: Callable[[Board],
                                  Node], static_eval_: Callable[[Board], int],
              prune_: Callable[[Node], Node]) -> Callable[[Board], int]:
    """Return a tree evaluation function"""
    def evaluate_(board: Board) -> State:
        return maximize1(maptree(static_eval_, prune_(gametree_(board))))

    return evaluate_


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
                print("skipped")
                for i in omit_(pot, seqs):
                    yield i
            else:
                yield m
                for i in omit_(m, seqs):
                    yield i

    return omit_


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


def replace_board(board, itr):
    for state in itr:
        yield State(board, state.score)


def map2_(func: Callable[[Node], State],
          subtrees: Iterator[Node]) -> Iterator[State]:
    assert subtrees is not None

    for subtree in subtrees:
        (state0, _) = subtree
        yield replace_board(state0.board, func(subtree))


def mapmin_(itr):
    return map(min, itr)


def mapmax_(itr):
    return map(max, itr)


def maximize2_(node: Node) -> Iterator[State]:
    """The max step of Minimax before max"""
    (state, subtrees) = node

    if subtrees is None:
        yield state
    else:
        #sutrees is an iterator of nodes
        for s in mapmin(map2_(minimize2_, subtrees)):
            yield s


def maximize2(node: Node) -> State:
    return max(maximize2_(node))


def minimize2_(node: Node) -> Iterator[State]:
    """The min step of Minimax before min"""
    (state, subtrees) = node

    if subtrees is None:
        yield state
    else:
        for s in mapmax(map2_(maximize2_, subtrees)):
            yield s


def minimize2(node: Node) -> State:
    return min(minimize2_(node))


def evaluate2(gametree_: Callable[[Board],
                                  Node], static_eval_: Callable[[Board], int],
              prune_: Callable[[Node], Node]) -> Callable[[Board], int]:
    """Return a tree evaluation function"""
    def evaluate_(board: Board) -> State:
        return maximize2(maptree(static_eval_, prune_(gametree_(board))))

    return evaluate_
