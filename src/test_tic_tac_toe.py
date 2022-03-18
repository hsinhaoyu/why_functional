from tic_tac_toe import init_board, moves, static_eval, display_board
from game import gametree, prune
from lazy_utils import tree_size, tree_depth, maptree, tree_labels


def test_gametree():
    print("\n\n## test_gametree: no pruning")
    b0 = init_board()
    t = gametree(moves, b0)
    d = tree_depth(t)
    print("depth=", d)


def test_gametree2():
    b0 = init_board()
    t = gametree(moves, b0)
    s = tree_size(t)
    print("size=", s)


def test_prune():
    print("\n\n## test_prune: after pruning")
    b0 = init_board()
    t = prune(5, gametree(moves, b0))
    d = tree_depth(t)
    print("depth=", d)


def test_prune2():
    b0 = init_board()
    t = prune(5, gametree(moves, b0))
    s = tree_size(t)
    print("size=", s)


def test_static_eval():
    """Apply static eval to one board"""
    print("\n## test_static_eval()")
    b0 = init_board()
    b0[4] = 0
    b0[5] = 1
    print()
    display_board(b0)

    v = static_eval_0(b0)
    print("score for player 0:", v)


def test_static_eval2():
    """Apply static eval to a game tree"""
    print("\n## test_static_eval2")

    def freq(lst):
        dict = {}
        for i in lst:
            if i in dict:
                dict[i] = dict[i] + 1
            else:
                dict[i] = 1
        return dict

    def show_freq(dict):
        k = dict.keys()
        k = sorted(k)
        for kk in k:
            print(f'{kk:10}     {dict[kk]}')

    b0 = init_board()
    t = prune(5, gametree(moves, b0))
    t = maptree(static_eval_0, t)
    t = list(tree_labels(t))
    show_freq(freq(t))
