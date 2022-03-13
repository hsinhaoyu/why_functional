import operator


def foldtree(f, g, a, tree_comp):
    """Apply two functions (f and g) to transform a tree."""
    if tree_comp == []:
        return a
    elif isinstance(tree_comp, list):
        # fold multiple subtrees
        subtree = tree_comp[0]
        rest = tree_comp[1:]
        return g(foldtree(f, g, a, subtree), foldtree(f, g, a, rest))
    else:
        assert isinstance(tree_comp, tuple)
        # fold a label with the subtrees
        (label, subtrees) = tree_comp
        return f(label, foldtree(f, g, a, subtrees))


def sumtree(tree):
    """Sum all labels in a tree."""
    add = operator.add
    return foldtree(add, add, 0, tree)


def tree_labels(tree):
    """Collect all labels of a tree into a list."""

    def cons(label, lst):
        return [label] + lst

    def append(lst1, lst2):
        return lst1 + lst2

    return foldtree(cons, append, [], tree)


def maptree(f, tree):
    """Map a function to all labels in a tree"""

    def cons(leaf, lst):
        return [leaf] + lst

    def mk_leaf(leaf, lst):
        return (f(leaf), lst)

    return foldtree(mk_leaf, cons, [], tree)
