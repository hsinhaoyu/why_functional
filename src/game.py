from lazy_utils import reptree, mk_tree, decompose_tree, maptree


def gametree(moves, board):
    return reptree(moves, board)


def prune(n: int, tree):
    (board, subtrees) = tree
    if n == 0:
        return mk_tree(board, iter([]))
    else:
        return mk_tree(board, map(lambda t: prune(n - 1, t), subtrees))


def maximize(gametree, depth):
    """The max step of Minimax"""
    ((board, score), subtrees) = gametree

    # if there is no subtree, return the score of the node
    # otherwise, find the max of the min's
    b, s = None, -100000
    for subtree in subtrees:
        ((board_, _), _) = subtree
        _, min_s = minimize(subtree, depth + 1)
        if min_s > s:
            b, s = board_, min_s

    if s == -100000:
        b, s = board, score

    if depth == 1:
        return b, s
    else:
        return None, s


def minimize(gametree, depth):
    """The min step of Minimax.
    A node in gametree is ((board, score), subtrees)
    Returns (board, score) with the minimal score
    """
    ((board, score), subtrees) = gametree

    # if there is no subtree, return the score of the node
    # otherwise, find the min of the max's
    #b, s = board, score
    #for (_, s_) in map(maximize, subtrees):
    #    if s_ < s:
    #        s = s_

    #return (b, s)
    b, s = None, 100000
    for subtree in subtrees:
        ((board_, _), _) = subtree
        _, max_s = maximize(subtree, depth + 1)
        if max_s < s:
            b, s = board_, max_s

    if s == 100000:
        b, s = board, score

    if depth == 1:
        return b, s
    else:
        return None, s


def evaluate1(board, moves, eval_func):
    """Evaluate a game position for player 1 with Minimax"""

    def maximize_(tree):
        return maximize(tree, 1)

    def eval_(board):
        return (board, eval_func(board))

    return maximize_(maptree(eval_, prune(5, gametree(moves, board))))
