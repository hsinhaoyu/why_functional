def reptree(f, label):
    """Appy a function f to all labels in a tree repeatedly."""
    return (label, map(lambda b: reptree(f, b), f(label)))


def gametree(moves, state):
    """Build a game tree given an initial state.
    moves is a function to return all leagal moves given a state.
    """
    return reptree(moves, state)


def prune(n, tree):
    (state, subtrees) = tree
    if n == 0:
        return (state, iter([]))
    else:
        return (state, map(lambda t: prune(n - 1, t), subtrees))
