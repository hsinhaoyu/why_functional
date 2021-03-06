from typing import Callable, Iterator, NamedTuple, Any, Optional, Union
from itertools import tee
import operator


def repeat_f(f: Callable[[float], float], a: float) -> Iterator[float]:
    """Infinite iterator: [a, f(a), f(f(a)), f(f(f(a))) ...]"""
    acc: float = a

    while True:
        yield acc
        acc = f(acc)


def within(esp: float, itr: Iterator[float]) -> Iterator[float]:
    """Stop if the next two iterations have a small delta."""
    a = next(itr)
    while True:
        b = next(itr)
        if abs(a - b) <= esp:
            yield b
        else:
            a = b


def relative(esp: float, itr: Iterator[float]) -> Iterator[float]:
    """Stop if the next two iterations have a small relative delta."""
    a = next(itr)
    while True:
        b = next(itr)
        if abs(a / b - 1) <= esp:
            yield b
        else:
            a = b


def repeat_itr(f: Callable[[Iterator], Iterator], i: Iterator) -> Iterator:
    """[i, f(i), f(f(i))...]"""
    acc: Iterator[float] = i

    while True:
        (i0, i1) = tee(acc)
        yield i0
        acc = f(i1)


Node = NamedTuple('Node', [('label', Any), ('subtrees', Optional[Iterator])])


def foldtree(f: Callable, g: Callable, a: Any, t: Union[Node, Iterator, None]):
    """Apply two functions (f and g) of two arguments to transform a lazy tree.
    f: fold a node's label to the folded subtrees
    g: fold a list of subtrees
    a: an initial constant
    t: a tree, an iterator of subtrees, or None
    """
    if t is None:
        return a
    elif isinstance(t, Node):
        (label, subtrees) = t
        return f(label, foldtree(f, g, a, subtrees))
    else:
        try:
            subtree = next(t)
            return g(foldtree(f, g, a, subtree), foldtree(f, g, a, t))
        except StopIteration:
            # as if the last item of an interator is None
            return a


def sumtree(t: Node) -> int:
    """Sum all the labels in a tree"""
    add = operator.add
    return foldtree(add, add, 0, t)


def tree_labels(t: Node) -> Iterator:
    """Visit all labels in a tree, return them in an iterator"""

    def f(label: Any, folded_subtrees: Optional[Iterator]) -> Iterator:
        yield label
        if folded_subtrees is not None:
            for item in folded_subtrees:
                yield item

    def g(folded_first: Iterator,
          folded_rest: Optional[Iterator]) -> Optional[Iterator]:
        for item in folded_first:
            yield item

        if folded_rest is not None:
            for item in folded_rest:
                yield item

    return foldtree(f, g, None, t)


def maptree(func: Callable, t: Node) -> Node:
    """Maps func to all labels in a tree. Returns another lazy tree"""

    def f(label: Any, folded_subtrees: Optional[Iterator]) -> Node:
        return Node(func(label), folded_subtrees)

    def g(folded_first: Node,
          folded_rest: Optional[Iterator]) -> Optional[Iterator]:
        yield folded_first
        if folded_rest is not None:
            for item in folded_rest:
                yield item

    return foldtree(f, g, None, t)


def tree_size(t: Node) -> int:
    """Return the number of labels in a lazy tree"""

    def f(label: Any, folded_subtrees: int) -> int:
        return 1 + folded_subtrees

    return foldtree(f, operator.add, 0, t)


def tree_depth(t: Node) -> int:
    """Return the length of the longist branch in the tree"""

    def f(label: Any, folded_subtrees: int) -> int:
        return 1 + folded_subtrees

    def g(folded_first: int, folded_rest: int) -> int:
        return max(folded_first, folded_rest)

    return foldtree(f, g, 0, t)


def reptree(f: Callable[[Any], Optional[Iterator[Any]]], label: Any) -> Node:
    """Appy a function f to a label repeatedly to create a tree.
    f(label) is a list of labels
    """

    def make_children(lst):
        if lst is None:
            # f produces nothing
            return None
        else:
            # else, apply f repeatedly to elements of lst
            return map(lambda b: reptree(f, b), lst)

    return Node(label, make_children(f(label)))


def prune(n: int, tree: Node) -> Node:
    """Remove nodes n levels below in the tree"""
    (board, subtrees) = tree

    if n == 0:
        return Node(board, None)
    elif subtrees is None:
        return Node(board, None)
    else:
        return Node(board, map(lambda t: prune(n - 1, t), subtrees))
