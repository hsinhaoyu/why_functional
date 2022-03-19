from lazy_utils import reptree, mk_tree, decompose_tree, maptree, prune


def gametree(moves):

    def gametree_(board):
        return reptree(moves, board)

    return gametree_


def maximize(gametree):
    """The max step of Minimax"""
    (score, subtrees) = gametree

    # if there is no subtree, return the score of the node
    # otherwise, find the max of the min's
    if subtrees is None:
        s = score
    else:
        s = max(map(minimize, subtrees))
    return s


def minimize(gametree):
    """The min step of Minimax.
    A node in gametree is ((board, score), subtrees)
    Returns (board, score) with the minimal score
    """
    (score, subtrees) = gametree

    # if there is no subtree, return the score of the node
    # otherwise, find the min of the max's
    if subtrees is None:
        s = score
    else:
        s = min(map(maximize, subtrees))
    return s


#def evaluate1(board, moves, eval_func):
#    """Evaluate a game position for player 1 with Minimax"""
#    return minimize(maptree(eval_func, prune(5, gametree(moves, board))))


def evaluate1(gametree_, eval_, prune_):

    def evaluate_(board):
        return minimize(maptree(eval_, prune_(gametree_(board))))

    return evaluate_


def ai_next_move(board, moves, eval_):
    """Given a board, return a board with AI's move.
    Note that AI is always player 1.
    """

    (_, subtrees) = gametree(moves, board)

    if subtrees is None:
        return None
    else:
        b, s = None, -1000000
        for next_move in subtrees:
            next_move_board = next_move[0]
            next_move_score = eval_(next_move_board)
            if next_move_score > s:
                b, s = next_move_board, next_move_score
        return b
