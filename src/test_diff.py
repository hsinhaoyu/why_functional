import pytest
from itertools import *
from math import cos

from diff import *


def f(x):
    return sin(x)


def test_diff1():
    x = 1.0
    h0 = 5.0
    d = diff1(h0, f, x)
    assert d == pytest.approx(cos(x))


def test_elimerror():
    print("\n## test_elimerror:")

    def f(x):
        return sin(x)

    seq1 = differentiate(5.0, f, 1.0)
    print("seq1:", list(islice(seq1, 20)))

    seq1 = differentiate(5.0, f, 1.0)
    seq2 = elimerror(2.0, seq1)

    print("seq2:", list(islice(seq2, 20)))


def test_improve():
    print("\n## test_improve")

    def f(x):
        return sin(x)

    seq1 = differentiate(2.0, f, 0.3)
    print("seq1:", list(islice(seq1, 20)))

    seq1 = differentiate(2.0, f, 0.3)
    seq2 = improve(seq1)

    print("seq2:", list(islice(seq2, 20)))


def test_diff2():
    def f(x):
        return sin(x)

    h0 = 1.0
    x = 0.3
    d = diff2(h0, f, x)
    assert d == pytest.approx(cos(x))


import pytest
from itertools import *
from math import cos

from diff import *


def f(x):
    return sin(x)


def test_diff1():
    x = 1.0
    h0 = 5.0
    d = diff1(h0, f, x)
    assert d == pytest.approx(cos(x))


def test_elimerror():
    print("\n## test_elimerror:")

    def f(x):
        return sin(x)

    seq1 = differentiate(5.0, f, 1.0)
    print("seq1:", list(islice(seq1, 20)))

    seq1 = differentiate(5.0, f, 1.0)
    seq2 = elimerror(2.0, seq1)

    print("seq2:", list(islice(seq2, 20)))


def test_improve():
    print("\n## test_improve")

    def f(x):
        return sin(x)

    seq1 = differentiate(2.0, f, 0.3)
    print("seq1:", list(islice(seq1, 20)))

    seq1 = differentiate(2.0, f, 0.3)
    seq2 = improve(seq1)

    print("seq2:", list(islice(seq2, 20)))


def test_diff2():
    def f(x):
        return sin(x)

    h0 = 1.0
    x = 0.3
    d = diff2(h0, f, x)
    assert d == pytest.approx(cos(x))
