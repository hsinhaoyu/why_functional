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


def test_prune():
    print("\n\n## test_prune: after pruning")
    b0 = init_board()
    t = prune(gametree(b0))
    d = tree_depth(t)
    print("depth=", d)


def test_prune2():
    b0 = init_board()
    t = prune(gametree(b0))
    s = tree_size(t)
    print("size=", s)


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


def test_static_eval():
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
    t = prune(gametree(b0))
    t = maptree(static_eval_state(0), t)
    t = tree_labels(t)  # collect all the states from the tree
    t = list(map(lambda s: s.score, t))  # extract just the scores
    show_freq(freq(t))


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
    print("## test_tree_eval()")
    b = [1, 0, 0, None, 0, None, 1, None, None]
    print("\nGiven this board, player 1 (O) to play")
    player = 1
    display_board(b)

    best_move = evaluate1(player)(b)
    print()
    print("O's best move:")
    display_board(best_move.board)

    # player 1 should be able to win the game in one move
    # so the score should be the winning score
    assert best_move.score == posinf


#@pytest.mark.skip(reason="skip skip skip")
