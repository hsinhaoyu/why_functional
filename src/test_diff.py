import pytest
from itertools import *

from diff import *


def f(x):
    return x * x


def test_diff1():
    d = diff1(5.0, f, 1.0)
    assert d == pytest.approx(2.0)


def test_elimerror():
    print("\n## test_elimerror:")

    def f(x):
        return x * x

    seq1 = differentiate(5.0, f, 1.0)
    print("seq1:", list(islice(seq1, 5)))

    seq1 = differentiate(5.0, f, 1.0)
    seq2 = elimerror(2.0, seq1)

    print("seq2:", list(islice(seq2, 5)))


def test_improve():
    print("\n## test_improve")

    def f(x):
        return x * x

    seq1 = differentiate(5.0, f, 0.3)
    print("seq1:", list(islice(seq1, 5)))

    seq1 = differentiate(5.0, f, 0.3)
    seq2 = improve(seq1)

    print("seq2:", list(islice(seq2, 5)))


def test_diff2():

    def f(x):
        return x * x

    d = diff2(5.0, f, 0.3)
    assert d == pytest.approx(0.6)
