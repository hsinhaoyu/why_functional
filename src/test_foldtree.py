from foldtree import *

my_tree2 = Node(1, [
    Node(2, [
        Node(3, []),
        Node(4, [Node(5, []), Node(6, [Node(7, [])])]),
        Node(8, [Node(9, [])])
    ]),
    Node(10, [Node(11, [])])
])

my_tree = Node(1, [Node(2, []), Node(3, [Node(4, [])])])


def test_sumtree():
    assert sumtree(Node(1, [])) == 1
    assert sumtree(my_tree) == 10
    assert sumtree(my_tree2) == sum(range(1, 12))


def test_tree_labels():
    assert tree_labels(Node(1, [])) == [1]
    assert tree_labels(my_tree) == [1, 2, 3, 4]
    assert tree_labels(my_tree2) == list(range(1, 12))


def test_maptree():
    res = maptree(lambda x: -1 * x, Node(1, []))
    assert res == Node(-1, [])

    res = maptree(lambda x: -1 * x, my_tree)
    res = tree_labels(res)
    assert res == [-1, -2, -3, -4]

    res = maptree(lambda x: -1 * x, my_tree2)
    res = tree_labels(res)
    assert res == [-1 * i for i in range(1, 12)]


def test_tree_size():
    assert tree_size(my_tree) == 4
    assert tree_size(Node(1, [])) == 1
    assert tree_size(my_tree2) == 11


def test_tree_depth():
    t = Node(1, [])
    assert tree_depth(t) == 1

    t = Node(1, [Node(2, [])])
    assert tree_depth(t) == 2

    assert tree_depth(my_tree) == 3

    assert tree_depth(my_tree2) == 5
