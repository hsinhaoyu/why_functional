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
