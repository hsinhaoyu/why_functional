from typing import Callable, Iterator


def next_sqrt_approx(n: float) -> Callable[[float], float]:
    """Next step in the approximation of sqrt(n) from x"""
    def next_approx_(x: float) -> float:
        return (x + n / x) / 2.0
    return next_approx_

def repeat(f: Callable[[float], float], a: float) -> Iterator[float]:
    """Infinite iterator: [a, f(a), f(f(a)), f(f(f(a))) ...]"""
    acc: float = a

    while True:
        yield acc
        acc = f(acc)

def newton_sqrt_(n: float, a: float) -> Iterator[float]:
    """An infinite iterator approximating sqrt(n) starting from a"""
    return repeat(next_sqrt_approx(n), a)

def within(esp: float, itr: Iterator) -> Iterator:
    """Stop if the next two iterations have a small delta"""
    while True:
        a = next(itr)
        b = next(itr)
        if abs(a - b) < esp:
            yield b

def newton_sqrt(n, a):
    r = within(0.00001, repeat(next_sqrt_approx(n), a))
    return next(r)
