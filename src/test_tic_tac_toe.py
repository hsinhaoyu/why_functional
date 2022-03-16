from tic_tac_toe import init_state, display_board, moves
from game import gametree, prune

b0 = init_state()
t = gametree(moves, b0)


def visit(t):
    (state, subtrees) = t
    display_board(state[0])
    n = next(subtrees)
    visit(n)


t2 = prune(3, t)
visit(t2)
