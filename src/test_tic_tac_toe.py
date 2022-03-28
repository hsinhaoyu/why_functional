from tic_tac_toe import init_board, moves, static_eval, display_board
from tic_tac_toe import who_plays, posinf, neginf, gametree, prune, won
from tic_tac_toe import static_eval_state
from tic_tac_toe import evaluate0, evaluate1, evaluate2
from lazy_utils import tree_size, tree_depth, maptree, tree_labels
import pytest


def test_who_plays():
    b = init_board()
    assert who_plays(b) == 0

    b[1] = 0
    assert who_plays(b) == 1


def test_moves():
    # there should be no legal move for 0 because 1 has already won
    b = [1, 0, 0, 1, 0, None, 1, None, None]
    assert moves(b) is None

    # there should be no legal move for 0 because 0 has already won
    b = [1, 0, 0, 1, 0, None, None, 0, 1]
    assert moves(b) is None

    # A draw. the board is full
    b = [1, 0, 1, 0, 0, 1, 0, 1, 0]
    assert moves(b) is None


def test_game_tree_structure():
    # Since player 0 has won, there should be no subtrees
    b = [1, 0, 0, 1, 0, None, None, 0, 1]
    assert won(b, 0) == True
    t = gametree(b)
    assert t[1] is None

    # Since player 1 has won, there should be no subtrees
    b = [1, 0, 0, 1, 0, None, 1, None, None]
    assert won(b, 1) == True
    t = gametree(b)
    assert t[1] is None

    # This is a draw. There should be no subtrees
    b = [1, 0, 1, 0, 0, 1, 0, 1, 0]
    assert won(b, 0) == False
    assert won(b, 1) == False
    t = gametree(b)
    assert t[1] is None


def test_static_eval_winning_condition():
    # evaluate for player 0
    eval_0 = static_eval(0)
    # evaluate for player 1
    eval_1 = static_eval(1)

    # player 0 won
    b = [1, 0, 0, 1, 0, None, None, 0, 1]
    assert eval_0(b) == posinf
    assert eval_1(b) == neginf

    # player 1 won
    b = [1, 0, 0, 1, 0, None, 1, None, None]
    assert eval_0(b) == neginf
    assert eval_1(b) == posinf


def test_gametree_evaluation():
    # player 0 has won
    b = [1, 0, 0, 1, 0, None, None, 0, 1]
    (score, subtrees) = maptree(static_eval(0), prune(gametree(b)))
    assert subtrees is None and score == posinf

    # player 1 has won
    b = [1, 0, 0, 1, 0, None, 1, None, None]
    (score, subtrees) = maptree(static_eval(0), prune(gametree(b)))
    assert subtrees is None and score == neginf

    # This is a draw
    b = [1, 0, 1, 0, 0, 1, 0, 1, 0]
    (score, subtrees) = maptree(static_eval(0), prune(gametree(b)))
    assert subtrees is None and score == 0


def test_tree_eval():
    # player 1 should be able to win the game in one move
    # so the score should be the winning score
    b = [1, 0, 0, None, 0, None, 1, None, None]
    player = 1
    score = evaluate0(player)(b)
    assert best_move.score == posinf


def test_tree_eval():
    # player 1 should be able to win the game in one move
    # so the score should be the winning score
    b = [1, 0, 0, None, 0, None, 1, None, None]
    best_move = evaluate1(player=1)(b)
    assert best_move.score == posinf

    # player 1 should block player 0's winning move
    b = [1, 0, None, None, 0, None, None, None, None]
    best_move = evaluate1(player=1)(b)
    assert best_move.board == [1, 0, None, None, 0, None, None, 1, None]

    # player 0's turn. It wins in 2 moves.
    b = [0, 1, None, None, 0, None, None, None, 1]
    best_move = evaluate1(player=0)(b)
    assert best_move.score == posinf

    # player 1's turn. It loses in 2 moves
    b = [0, 1, None, None, 0, None, 0, None, 1]
    best_move = evaluate1(player=1)(b)
    assert best_move.score == neginf
