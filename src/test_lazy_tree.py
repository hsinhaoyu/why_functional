from lazy_utils import *


def mk_tree_(label, lst):
    """A throw-away function just for this example"""
    if lst is None:
        return (label, None)
    else:
        return (label, iter(lst))


def mk_test_tree():
    my_tree = mk_tree_(1,
                       [mk_tree_(2, None),
                        mk_tree_(3, [mk_tree_(4, None)])])
    return my_tree


def test_tree_labels():
    t = mk_test_tree()
    i = tree_labels(t)
    assert list(i) == [1, 2, 3, 4]


def test_maptree():

    def f(n):
        return -1 * n

    t = mk_test_tree()
    t = maptree(f, t)
    t = tree_labels(t)
    assert list(t) == [-1, -2, -3, -4]


def test_tree_size():
    t = mk_test_tree()
    s = tree_size(t)
    assert s == 4


def test_tree_depth():
    t = mk_test_tree()
    d = tree_depth(t)
    assert d == 3
