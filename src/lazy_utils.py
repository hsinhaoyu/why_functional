from typing import Callable, Iterator, Tuple
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


def tree_labels(t):
    label, subtrees = t
    yield label
    if subtrees is not None:
        for i in subtrees:
            for j in tree_labels(i):
                yield j


def mapforest_(f, forest):
    assert forest is not None
    for t in forest:
        yield maptree(f, t)


def maptree(f, t):
    label, subtrees = t
    if subtrees is None:
        return (f(label), None)
    else:
        return (f(label), mapforest_(f, subtrees))


def tree_size(t):
    label, subtrees = t

    if subtrees is None:
        return 1
    else:
        return 1 + sum(map(tree_size, subtrees))


def tree_depth(t):

    def tree_depth_(t, d):
        label, subtrees = t

        if subtrees is None:
            return d
        else:
            try:
                return max(map(lambda t: tree_depth_(t, d + 1), subtrees))
            except ValueError:
                print(label, subtrees)

    return tree_depth_(t, 1)


def reptree(f: Callable, label) -> Tuple:
    """Appy a function f to a label repeatedly to create a tree.
    f(label) is a list of labels
    """

    def make_children(lst):
        if lst == None:
            # f produces nothing
            return None
        else:
            # else, apply f repeatedly to elements of lst
            return map(lambda b: reptree(f, b), lst)

    return (label, make_children(f(label)))


def prune(n: int, tree: Tuple):
    """Remove nodes n levels below in the tree"""
    (board, subtrees) = tree

    if n == 0:
        return (board, None)
    elif subtrees is None:
        return (board, None)
    else:
        return (board, map(lambda t: prune(n - 1, t), subtrees))
