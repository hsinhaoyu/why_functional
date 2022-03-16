from lazy_utils import *


def mk_tree_(label, lst):
    """A throw-away function just for this example"""
    return (label, iter(lst))


my_tree = mk_tree_(1, [mk_tree_(2, []), mk_tree_(3, [mk_tree_(4, [])])])


def test_tree_labels():
    t = tree_labels(my_tree)
    assert list(t) == [1, 2, 3, 4]


my_tree2 = mk_tree_(1, [mk_tree_(2, []), mk_tree_(3, [mk_tree_(4, [])])])


def test_maptree():

    def f(n):
        return -1 * n

    t = maptree(f, my_tree2)
    t = tree_labels(t)
    assert list(t) == [-1, -2, -3, -4]
