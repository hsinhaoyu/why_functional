from game import *


def test_minleq():
    assert minleq(None, 10) == 10

    # not sure if this is the right behavior
    assert minleq(iter([]), 10) == 10

    # looking for a min greater than potential max 5
    itr = iter([7])
    assert minleq(itr, 5) == 7

    # looking for a min greater than potential max 8
    itr = iter([7])
    assert minleq(itr, 8) is True

    # looking for a min greater than potential max 20
    # as soon as we encounter 3, we can stop
    # because the min must be smaller than 3
    itr = iter([3, 2, 5, 10, 1, 6])
    assert minleq(itr, 20) is True

    # looking for a min greater than potential max 10
    itr = iter([3, 2, 5, 10, 1, 6])
    assert minleq(itr, 10) is True

    # looking for a min greater than potential max 1
    itr = iter([3, 2, 5, 10, 1, 6])
    assert minleq(itr, 1) is True

    # looking for a min greater than potential max 0
    # return the min of itr, which can be the new max
    itr = iter([3, 2, 5, 10, 1, 6])
    assert minleq(itr, 0) == 1


def test_maxgeq():
    assert maxgeq(None, 10) == 10

    # not sure if this is the right behavior
    assert maxgeq(iter([]), 10) == 10

    # looking for a max smaller than potential min 5
    itr = iter([7])
    assert maxgeq(itr, 5) is True

    # looking for a max smaller than potential min 8
    # 7 can be the new min
    itr = iter([7])
    assert maxgeq(itr, 8) == 7

    # looking for a max smaller than potential min 20
    # it is the min of iter 10, which can be the new min
    itr = iter([3, 2, 5, 10, 1, 6])
    assert maxgeq(itr, 20) == 10

    # looking for a max smaller than potential min 10
    # as soon as we found 10, we don't need to go further
    itr = iter([3, 2, 5, 10, 1, 6])
    assert maxgeq(itr, 10) is True

    # looking for a max smaller than potential min 1
    # as soon as we found 3, we don't need to go further
    itr = iter([3, 2, 5, 10, 1, 6])
    assert maxgeq(itr, 1) is True

    # looking for a max smaller than potential min 0
    # as soon as we found 3, we don't need to go further
    itr = iter([3, 2, 5, 10, 1, 6])
    assert maxgeq(itr, 0) is True


def test_omit_max():
    seqs = iter([])
    assert list(omit_max(-1, seqs)) == []

    seqs = iter([iter([1])])
    assert list(omit_max(-1, seqs)) == [1]

    seqs = iter([iter([1])])
    assert list(omit_max(3, seqs)) == []

    # not sure if this is the right behavior
    seqs = iter([iter([])])
    assert list(omit_max(3, seqs)) == [3]

    seqs = iter([iter([1, 2]), iter([0, 10]), iter([10, -3])])
    assert list(omit_max(-1, seqs)) == [1]

    seqs = iter([iter([1, 2]), iter([0, 10]), iter([3, 20]), iter([1, 100])])
    assert list(omit_max(-1, seqs)) == [1, 3]


def test_omit_min():
    seqs = iter([])
    assert list(omit_min(-1, seqs)) == []

    seqs = iter([iter([1])])
    assert list(omit_min(-1, seqs)) == []

    seqs = iter([iter([1])])
    assert list(omit_min(3, seqs)) == [1]

    # not sure if this is the right behavior
    seqs = iter([iter([])])
    assert list(omit_min(3, seqs)) == [3]

    seqs = iter([iter([1, 2]), iter([0, 10]), iter([10, -3])])
    assert list(omit_min(-1, seqs)) == []

    seqs = iter([iter([1, 2]), iter([0, 10]), iter([3, 20]), iter([1, 100])])
    assert list(omit_min(-1, seqs)) == []


def test_mapmin():
    seqs = iter([iter([1, 2])])
    assert list(mapmin(seqs)) == [1]

    seqs = iter([iter([1, 2]), iter([0, 10]), iter([10, -3])])
    assert list(mapmin(seqs)) == [1]

    seqs = iter([iter([1, 2]), iter([0, 10]), iter([3, 20]), iter([1, 100])])
    assert list(mapmin(seqs)) == [1, 3]


def test_mapmax():
    seqs = iter([iter([1, 2])])
    assert list(mapmax(seqs)) == [2]

    seqs = iter([iter([1, 2]), iter([0, 10]), iter([10, -3])])
    assert list(mapmax(seqs)) == [2]

    seqs = iter([iter([1, 2]), iter([0, 10]), iter([3, 20]), iter([1, 100])])
    assert list(mapmax(seqs)) == [2]
