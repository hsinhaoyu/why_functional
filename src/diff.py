from typing import Callable, Iterator
from lazy_utils import *

def easydiff(f: Callable[[float], float], x: float) -> float:
    def easydiff_(h: float):
        return (f(x + h) - f(x)) / h

    return easydiff_

def half(x: float) -> float:
    return x / 2.0

def differentiate_(h0: float, f: Callable[[float], float], x: float) -> Iterator:
    return map(easydiff(f, x), repeat(half, h0))

def differentiate(h0: float, f: Callable[[float], float], x: float) -> Iterator:
    d = differentiate_(h0, f, x)
    return next(within(0.000000001, d))
