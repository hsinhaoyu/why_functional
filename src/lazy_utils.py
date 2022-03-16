from typing import Callable, Iterator
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


def mk_tree(label, subtrees):
    return (label, subtrees)


def decompose_tree(t):
    try:
        label, subtrees = t[0], t[1]
        return label, subtrees
    except ValueError:
        raise Exception("Not a tree")


def tree_labels(t):
    label, subtrees = decompose_tree(t)
    yield label
    for i in subtrees:
        for j in tree_labels(i):
            yield j


def mapforest_(f, forest):
    for t in forest:
        yield maptree(f, t)


def maptree(f, t):
    label, subtrees = decompose_tree(t)
    return mk_tree(f(label), mapforest_(f, subtrees))


def tree_size(t):
    label, subtrees = decompose_tree(t)

    count = 1
    for t in subtrees:
        count = count + tree_size(t)
    return count


def tree_depth(t):

    def tree_depth_(t, d):
        label, subtrees = decompose_tree(t)

        mx = d
        for t_ in subtrees:
            mx = max(mx, tree_depth_(t_, d + 1))
        return mx

    return tree_depth_(t, 1)


def reptree(f, label):
    """Appy a function f to all labels in a tree repeatedly."""
    return mk_tree(label, map(lambda b: reptree(f, b), f(label)))
