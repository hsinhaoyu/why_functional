from tic_tac_toe import init_board, moves, static_eval
from game import gametree, prune
from lazy_utils import tree_size, tree_depth


def test_gametree():
    b0 = init_board()
    t = gametree(moves, b0)
    d = tree_depth(t)
    print("\nBefore pruning:")
    print("depth=", d)


def test_gametree2():
    b0 = init_board()
    t = gametree(moves, b0)
    s = tree_size(t)
    print("\nBefore pruning:")
    print("size=", s)


def test_prune():
    b0 = init_board()
    t = prune(4, gametree(moves, b0))
    d = tree_depth(t)
    print("\nAfter pruning:")
    print("depth=", d)


def test_prune2():
    b0 = init_board()
    t = prune(5, gametree(moves, b0))
    s = tree_size(t)
    print("\nAfter pruning:")
    print("size=", s)


def test_static_eval():
    b0 = init_board()
    b0[4] = 0
    print(b0)

    v = static_eval(b0)
    print(v)
