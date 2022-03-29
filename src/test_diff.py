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


def test_diff2():
    h0, x = 1.0, 0.3
    d = diff2(h0, f, x)
    assert d == pytest.approx(cos(x))


def test_repeat_improve():

    def f(x):
        return sin(x)

    d = differentiate(1.0, f, 0.3)
    d4 = improve(improve(improve(improve(d))))
    seq1 = list(islice(d4, 5))

    d = differentiate(1.0, f, 0.3)
    dx = repeat_itr(improve, d)
    next(dx)
    next(dx)
    next(dx)
    next(dx)
    seq2 = list(islice(next(dx), 5))

    assert seq1 == seq2


def test_diff3():
    h0, x = 1.0, 0.3
    d = diff3(h0, f, x)
    assert d == pytest.approx(cos(x))
