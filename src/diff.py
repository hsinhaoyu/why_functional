import copy
from math import log2, sin
from typing import Callable, Iterator
from itertools import chain, tee
from lazy_utils import repeat_f, within

esp = 0.000000001  # a small number that's used to call within()


def easydiff(f: Callable[[float], float], x: float) -> float:
    def easydiff_(h: float):
        return (f(x + h) - f(x)) / h

    return easydiff_


def half(x: float) -> float:
    return x / 2.0


def differentiate(h0: float, f: Callable[[float], float],
                  x: float) -> Iterator:
    return map(easydiff(f, x), repeat_f(half, h0))


def diff1(h0: float, f: Callable[[float], float], x: float) -> float:
    d = within(esp, differentiate(h0, f, x))
    return next(d)


def elimerror__(n: int, itr: Iterator) -> Iterator:
    a, b = next(itr), next(itr)
    p: float = 2.0**n
    c: float = (b * p - a) / (p - 1.0)

    for x in chain([c], elimerror(n, chain([b], itr))):
        yield x


def elimerror(n, itr):
    a = next(itr)
    while True:
        b = next(itr)
        p = 2.0**n
        c = (b * p - a) / (p - 1.0)
        yield c
        a = b


def order(itr: Iterator) -> int:
    a, b, c = next(itr), next(itr), next(itr)
    return round(log2((a - c) / (b - c) - 1.0))


def improve(itr: Iterator) -> Iterator:
    (itr1, itr2) = tee(itr)
    n: int = order(itr1)
    return elimerror(n, itr2)


def diff2(h0: float, f: Callable[[float], float], x: float) -> float:
    d = within(esp, improve(differentiate(h0, f, x)))
    return next(d)


def super__(itr):
    return repeat_itr(improve, itr)


def second(itr):
    next(itr)
    return next(itr)


def super_(itr):
    return map(second, super__(itr))


def super_differentiate(h0, f, x):
    return super_(differentiate(h0, f, x))
