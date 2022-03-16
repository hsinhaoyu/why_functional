from lazy_utils import reptree, mk_tree


def gametree(moves, board):
    return reptree(moves, board)


def prune(n, tree):
    (board, subtrees) = tree
    if n == 0:
        return mk_tree(board, iter([]))
    else:
        return mk_tree(board, map(lambda t: prune(n - 1, t), subtrees))
