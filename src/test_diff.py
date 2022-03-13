import pytest
from itertools import *
from math import cos, sin

from lazy_utils import *
from diff import *


def f(x: float) -> float:
    return sin(x)


def test_diff1():
    h0, x = 5.0, 1.0
    d = diff1(h0, f, x)
    assert d == pytest.approx(cos(x))


def test_elimerror():
    print("\n## test_elimerror:")

    h0, x, n = 5.0, 1.0, 2

    seq1 = differentiate(h0, f, x)
    print("seq1:", list(islice(seq1, 20)))

    seq1 = differentiate(h0, f, x)
    seq2 = elimerror(n, seq1)

    print("seq2:", list(islice(seq2, 20)))


def test_improve():
    print("\n## test_improve")

    h0, x = 2.0, 0.3

    seq1 = differentiate(h0, f, x)
    print("seq1:", list(islice(seq1, 20)))

    seq1 = differentiate(h0, f, x)
    seq2 = improve(seq1)

    print("seq2:", list(islice(seq2, 20)))


def test_diff2():
    h0, x = 1.0, 0.3
    d = diff2(h0, f, x)
    assert d == pytest.approx(cos(x))


def test_repeat_improve():
    print("\n## test_repeat_improve():")

    def f(x):
        return sin(x)

    d = differentiate(1.0, f, 0.3)
    d4 = improve(improve(improve(improve(d))))
    seq1 = list(islice(d4, 5))
    print("seq1:", seq1)

    d = differentiate(1.0, f, 0.3)
    dx = repeat_itr(improve, d)
    next(dx)
    next(dx)
    next(dx)
    next(dx)
    seq2 = list(islice(next(dx), 5))
    print("seq2:", seq2)

    assert seq1 == seq2


def test_diff3():
    h0, x = 1.0, 0.3
    d = diff3(h0, f, x)
    assert d == pytest.approx(cos(x))
