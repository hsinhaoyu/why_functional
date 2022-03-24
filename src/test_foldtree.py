from foldtree import *

my_tree2 = (1, [(2, [(3, []), (4, [(5, []), (6, [(7, [])])]), (8, [(9, [])])]),
                (10, [(11, [])])])

my_tree = (1, [(2, []), (3, [(4, [])])])


def test_sumtree():
    assert sumtree(my_tree) == 10
    assert sumtree(my_tree2) == sum(range(1, 12))


def test_tree_labels():
    assert tree_labels(my_tree) == [1, 2, 3, 4]
    assert tree_labels(my_tree2) == list(range(1, 12))


def test_maptree():
    res = maptree(lambda x: -1 * x, my_tree)
    res = tree_labels(res)
    assert res == [-1, -2, -3, -4]

    res = maptree(lambda x: -1 * x, my_tree2)
    res = tree_labels(res)
    assert res == [-1 * i for i in range(1, 12)]


def test_tree_size():
    assert tree_size(my_tree) == 4
    assert tree_size((1, [])) == 1
    assert tree_size(my_tree2) == 11


def test_tree_depth():
    t = (1, [])
    assert tree_depth(t) == 1

    t = (1, [(2, [])])
    assert tree_depth(t) == 2

    assert tree_depth(my_tree) == 3

    assert tree_depth(my_tree2) == 5
