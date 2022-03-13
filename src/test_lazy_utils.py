import pytest
from lazy_utils import *


def test_repeat_f():
    r = repeat_f(lambda n: n + 1, 0)
    v1, v2, v3 = next(r), next(r), next(r)
    assert v1 == 0
    assert v2 == 1
    assert v3 == 2
