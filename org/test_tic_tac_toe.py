def test_who_plays():
    b = init_board()
    assert who_plays(b) == 0

    b[1] = 0
    assert who_plays(b) == 1

    b[2] = 1
    assert who_plays(b) == 0

def test_moves():

    # there should be no legal move for 0 because 1 has already won
    b = [1, 0, 0, 1, 0, None, 1, None, None]
    assert moves(b) is None

def test_who_plays():
    b = init_board()
    assert who_plays(b) == 0

    b[1] = 0
    assert who_plays(b) == 1

    b[2] = 1
    assert who_plays(b) == 0

def test_moves():

    # there should be no legal move for 0 because 1 has already won
    b = [1, 0, 0, 1, 0, None, 1, None, None]
    assert moves(b) is None

def test_who_plays():
    print("who plays?")
    b = init_board()
    assert who_plays(b) == 0

    b[1] = 0
    assert who_plays(b) == 1

    b[2] = 1
    assert who_plays(b) == 0

def test_moves():

    # there should be no legal move for 0 because 1 has already won
    b = [1, 0, 0, 1, 0, None, 1, None, None]
    assert moves(b) is None
