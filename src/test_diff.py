import pytest
from itertools import *

from diff import *


def f(x):
    return x * x


def test_differentiate():
    a = differentiate(5.0, f, 1.0)
    assert a == pytest.approx(2.0)


def test_elimerror():
    print("\n## test_elimerror\n")

    def f(x):
        return x * x

    seq1 = differentiate_(5.0, f, 1.0)
    print("seq1:", list(islice(seq1, 5)))

    seq1 = differentiate_(5.0, f, 1.0)
    seq2 = elimerror(2.0, seq1)

    print("seq2:", list(islice(seq2, 5)))
