import pytest
from foldtree import *

my_tree = (1, [(2, []), (3, [(4, [])])])


def test_sumtree():
    assert sumtree(my_tree) == 10


def test_tree_labels():
    assert tree_labels(my_tree) == [1, 2, 3, 4]


def test_maptree():
    res = maptree(lambda x: -1 * x, my_tree)
    res = tree_labels(res)
    assert res == [-1, -2, -3, -4]
