from typing import Callable, Iterator, NamedTuple, Any, Optional
from itertools import tee


def repeat_f(f: Callable[[float], float], a: float) -> Iterator[float]:
    """Infinite iterator: [a, f(a), f(f(a)), f(f(f(a))) ...]"""
    acc: float = a

    while True:
        yield acc
        acc = f(acc)


def within(esp: float, itr: Iterator[float]) -> Iterator[float]:
    """Stop if the next two iterations have a small delta."""
    while True:
        a = next(itr)
        b = next(itr)
        if abs(a - b) < esp:
            yield b


def repeat_itr(f: Callable[[Iterator], Iterator], i: Iterator) -> Iterator:
    """[i, f(i), f(f(i))...]"""
    acc: Iterator[float] = i

    while True:
        (i0, i1) = tee(acc)
        yield i0
        acc = f(i1)


Node = NamedTuple('Node', [('label', Any), ('subtrees', Optional[Iterator])])


def tree_labels(t: Node) -> Iterator[Any]:
    label, subtrees = t
    yield label
    if subtrees is not None:
        for i in subtrees:
            for j in tree_labels(i):
                yield j


def mapforest_(f: Callable[[Any], Any],
               forest: Optional[Iterator]) -> Iterator[Node]:
    assert forest is not None
    for t in forest:
        yield maptree(f, t)


def maptree(f: Callable[[Any], Any], t: Node) -> Node:
    label, subtrees = t
    if subtrees is None:
        return Node(f(label), None)
    else:
        return Node(f(label), mapforest_(f, subtrees))


def tree_size(t: Node) -> int:
    """The number of labels in a lazy tree"""
    label, subtrees = t

    if subtrees is None:
        return 1
    else:
        return 1 + sum(map(tree_size, subtrees))


def tree_depth(t: Node) -> int:
    """The maximum depth of a lazy tree"""

    def tree_depth_(t: Node, d: int) -> int:
        label, subtrees = t

        if subtrees is None:
            return d
        else:
            return max(map(lambda t: tree_depth_(t, d + 1), subtrees))

    return tree_depth_(t, 1)


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
