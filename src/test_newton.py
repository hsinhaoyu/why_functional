import pytest
from newton import *

def test_next_sqrt_approx():
    f = next_sqrt_approx(10.0)
    assert f(2.0) == pytest.approx(3.5)

def test_repeat():
    r = repeat(lambda n: n + 1, 0)
    v1, v2, v3 = next(r), next(r), next(r)
    assert v1 == 0
    assert v2 == 1
    assert v3 == 2

def test_newton_sqrt_():
    r = newton_sqrt_(10.0, 2.0)
    v1, v2, v3 = next(r), next(r), next(r)
    assert v1 == pytest.approx(2.0)
    assert v2 == pytest.approx(3.5)
    assert v3 == pytest.approx(3.178571428571429)
