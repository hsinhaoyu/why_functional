from lazy_utils import *


def mk_test_tree2():
    my_tree = mk_tree_(1, [
        mk_tree_(2, [
            mk_tree_(3, None),
            mk_tree_(4, [mk_tree_(5, None),
                         mk_tree_(6, [mk_tree_(7, None)])]),
            mk_tree_(8, [mk_tree_(9, None)])
        ]),
        mk_tree_(10, [mk_tree_(11, None)])
    ])
    return my_tree


def mk_tree_(label, lst):
    """A throw-away function just for this example"""
    if lst is None:
        return Node(label, None)
    else:
        return Node(label, iter(lst))


def mk_test_tree():
    my_tree = mk_tree_(1,
                       [mk_tree_(2, None),
                        mk_tree_(3, [mk_tree_(4, None)])])
    return my_tree


def test_sumtree():
    t = mk_test_tree()
    assert sumtree(t) == 10

    t = mk_test_tree2()
    assert sumtree(t) == sum(range(1, 12))


def tree_labels(t: Node) -> Iterator:

    def f(label: Any, folded_subtrees: Iterator) -> Iterator:
        yield label
        for item in folded_subtrees:
            yield item

    def g(folded_first: Iterator, folded_rest: Iterator) -> Iterator:
        for item in folded_first:
            yield item
        for item in folded_rest:
            yield item

    return foldtree(f, g, [], t)


def test_tree_labels():
    t = mk_test_tree()
    i = tree_labels(t)
    assert list(i) == [1, 2, 3, 4]

    t = mk_test_tree2()
    i = tree_labels(t)
    assert list(i) == list(range(1, 12))


def test_maptree():

    def f(n):
        return -1 * n

    t = mk_test_tree()
    t = maptree(f, t)
    t = tree_labels(t)
    assert list(t) == [-1, -2, -3, -4]

    t = mk_test_tree2()
    res = maptree(lambda x: -1 * x, t)
    res = tree_labels(res)
    assert list(res) == [-1 * i for i in range(1, 12)]


def test_tree_size():
    t = mk_tree_(1, None)
    assert tree_size(t) == 1

    t = mk_test_tree()
    assert tree_size(t) == 4

    t = mk_test_tree2()
    assert tree_size(t) == 11


def test_tree_depth():
    t = mk_tree_(1, None)
    assert tree_depth(t) == 1

    t = mk_tree_(1, [mk_tree_(2, None)])
    assert tree_depth(t) == 2

    t = mk_test_tree()
    assert tree_depth(t) == 3

    t = mk_test_tree2()
    assert tree_depth(t) == 5
