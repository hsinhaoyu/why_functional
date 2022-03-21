from math import log2
from typing import Callable, Iterator
from itertools import tee
from lazy_utils import repeat_f, within, repeat_itr

esp = 0.0000000001  # a small number that's used to call within()


def easydiff(f: Callable[[float], float],
             x: float) -> Callable[[float], float]:

    def easydiff_(h: float) -> float:
        return (f(x + h) - f(x)) / h

    return easydiff_


def half(x: float) -> float:
    """Half the value"""
    return x / 2.0


def differentiate(h0: float, f: Callable[[float], float],
                  x: float) -> Iterator:
    """An interator of 1st-order approximation of f'(x) with initial h0"""
    return map(easydiff(f, x), repeat_f(half, h0))


def diff1(h0: float, f: Callable[[float], float], x: float) -> float:
    """Approximate f'(x), with an initial h0."""
    d = within(esp, differentiate(h0, f, x))
    return next(d)


def elimerror(n: int, itr: Iterator[float]) -> Iterator[float]:
    """Reduce the error of sequence approx. derivative, assuming order n."""
    a = next(itr)
    while True:
        b = next(itr)
        p = 2.0**n
        c = (b * p - a) / (p - 1.0)
        yield c
        a = b


def order(itr: Iterator[float]) -> int:
    """Estimate the order for elimerror()."""
    a, b, c = next(itr), next(itr), next(itr)
    return round(log2((a - c) / (b - c) - 1.0))


def improve(itr: Iterator[float]) -> Iterator[float]:
    """Improve the congergence of sequence approx. derivative."""
    (itr1, itr2) = tee(itr)
    n: int = order(itr1)
    return elimerror(n, itr2)


def diff2(h0: float, f: Callable[[float], float], x: float) -> float:
    """Approximate f'(x), with an initial h0."""
    d = within(esp, improve(differentiate(h0, f, x)))
    return next(d)


def second(itr: Iterator[float]) -> float:
    """Returns the second item in an iterator."""
    next(itr)
    return next(itr)


def super_improve(itr: Iterator[float]) -> Iterator[float]:
    """Improve the convergenve of a sequence approx. derivative."""
    return map(second, repeat_itr(improve, itr))


def diff3(h0: float, f: Callable[[float], float], x: float) -> float:
    """Approximate f'(x), with an initial h0."""
    d = within(esp, super_improve(differentiate(h0, f, x)))
    return next(d)
