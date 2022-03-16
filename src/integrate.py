from typing import Callable, Iterator, Tuple
from lazy_utils import within
from diff import improve

esp = 0.0000000001  # a small number that's used to call within()


def easyintegrate(f: Callable[[float], float], a: float, b: float) -> float:
    """Calculate the area under a linear function f between and and b."""
    return (f(a) + f(b)) * (b - a) / 2.0


def addpair(pair: Tuple[float, float]) -> float:
    """(a, b) -> a + b """
    (v1, v2) = pair
    return v1 + v2


def integrate_(f: Callable[[float], float], a: float,
               b: float) -> Iterator[float]:
    """Return an iterator that approximates intergral(f) in (a, b)."""
    yield easyintegrate(f, a, b)
    mid = (a + b) / 2.0
    s = map(addpair, zip(integrate_(f, a, mid), integrate_(f, mid, b)))
    for i in s:
        yield i


def integrate1(f: Callable[[float], float], a: float, b: float) -> float:
    """Calculate the integral of f between a and b."""
    d = within(esp, integrate_(f, a, b))
    return next(d)


def integ(f: Callable[[float], float], a: float, b: float, fa: float,
          fb: float) -> Iterator[float]:
    """Like integrate_, but with pre-calculated f(a) and f(b)."""
    yield (fa + fb) * (b - a) / 2.0
    m = (a + b) / 2.0
    fm = f(m)
    s = map(addpair, zip(integ(f, a, m, fa, fm), integ(f, m, b, fm, fb)))
    for i in s:
        yield i


def integrate2(f: Callable[[float], float], a: float, b: float) -> float:
    d = within(esp, integ(f, a, b, f(a), f(b)))
    return next(d)


def integrate3(f: Callable[[float], float], a: float, b: float) -> float:
    d = within(esp, improve(integ(f, a, b, f(a), f(b))))
    return next(d)
