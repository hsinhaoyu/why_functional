from math import sin, pi
import pytest
from integrate import *


def f(x):
    return sin(x)


def test_integrate1():
    print("\n## test_integrate1()")
    a, b = 0.0, pi
    d = integrate1(f, a, b)
    assert d == pytest.approx(2.0)


def test_integrate2():
    print("\n## test_integrate2()")
    a, b = 0.0, pi
    d = integrate2(f, a, b)
    assert d == pytest.approx(2.0)


def test_integrate3():
    print("\n## test_integrate3()")
    a, b = 0.0, pi
    d = integrate3(f, a, b)
    assert d == pytest.approx(2.0)
