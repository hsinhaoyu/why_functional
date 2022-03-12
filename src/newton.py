from typing import Callable, Iterator
from lazy_utils import *


def next_sqrt_approx(n: float) -> Callable[[float], float]:
    """Next step in the approximation of sqrt(n) from x"""
    def next_approx_(x: float) -> float:
        return (x + n / x) / 2.0

    return next_approx_


def newton_sqrt_(n: float, a: float) -> Iterator[float]:
    """An infinite iterator approximating sqrt(n) starting from a"""
    return repeat_f(next_sqrt_approx(n), a)


def newton_sqrt(n, a):
    r = within(0.00001, repeat_f(next_sqrt_approx(n), a))
    return next(r)


from typing import Callable, Iterator
from lazy_utils import *


def next_sqrt_approx(n: float) -> Callable[[float], float]:
    """Next step in the approximation of sqrt(n) from x"""
    def next_approx_(x: float) -> float:
        return (x + n / x) / 2.0

    return next_approx_


def newton_sqrt_(n: float, a: float) -> Iterator[float]:
    """An infinite iterator approximating sqrt(n) starting from a"""
    return repeat_f(next_sqrt_approx(n), a)


def newton_sqrt(n, a):
    r = within(0.00001, repeat_f(next_sqrt_approx(n), a))
    return next(r)
