from typing import Callable, Iterator


def repeat(f: Callable[[float], float], a: float) -> Iterator[float]:
    """Infinite iterator: [a, f(a), f(f(a)), f(f(f(a))) ...]"""
    acc: float = a

    while True:
        yield acc
        acc = f(acc)

def within(esp: float, itr: Iterator) -> Iterator:
    """Stop if the next two iterations have a small delta"""
    while True:
        a = next(itr)
        b = next(itr)
        if abs(a - b) < esp:
            yield b
