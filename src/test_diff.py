import pytest
from diff import *

def f(x):
    return x * x

def test_differentiate():
    a = differentiate(5.0, f, 1.0)
    assert a == pytest.approx(2.0)
