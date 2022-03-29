import math
import pytest
from newton import *


def test_newton_sqrt_():
    r = newton_sqrt_(10.0, 2.0)
    v1, v2, v3 = next(r), next(r), next(r)
    assert v1 == pytest.approx(2.0)
    assert v2 == pytest.approx(3.5)
    assert v3 == pytest.approx(3.178571428571429)


def test_newton_sqrt():
    res = newton_sqrt(10.0, 2.0)
    assert res == pytest.approx(math.sqrt(10.0))


def test_newton_sqrt_relative():
    res = newton_sqrt_relative(10.0, 2.0)
    assert res == pytest.approx(math.sqrt(10.0))
