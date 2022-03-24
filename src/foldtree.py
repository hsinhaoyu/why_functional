from typing import Tuple, Callable, Any, List
import operator


def foldtree(f: Callable, g: Callable, a: Any, t: Tuple):
    """Apply two functions (f and g) of two arguments to transform a tree.
    f: combine the label of a node to its subtrees
    g: combine the subtrees of a node
    a: an initial constant
    t: a tree, a list of subtrees, or []
    """
    if t == []:
        return a
    elif isinstance(t, tuple):
        (label, subtrees) = t
        return f(label, foldtree(f, g, a, subtrees))
    else:
        # fold multiple subtrees
        subtree = t[0]
        rest = t[1:]
        return g(foldtree(f, g, a, subtree), foldtree(f, g, a, rest))


def sumtree(t: Tuple) -> int:
    """Sum all labels in a tree."""
    f = operator.add
    g = operator.add
    return foldtree(f, g, 0, t)


def tree_labels(t):
    """Collect all labels of a tree into a list."""

    def f(label: Any, folded_subtrees: List) -> List:
        return [label] + folded_subtrees

    def g(folded_first: List, folded_rest: List) -> List:
        return folded_first + folded_rest

    return foldtree(f, g, [], t)


def maptree(func: Callable, t: Tuple) -> Tuple:
    """Map a function to all labels in a tree.
    Return a new tree.
    """

    def f(label: Any, folded_subtrees: List) -> Tuple:
        return (func(label), folded_subtrees)

    def g(folded_first: Any, folded_rest: List) -> List:
        return [folded_first] + folded_rest

    return foldtree(f, g, [], t)


def tree_size(t: Tuple) -> int:
    """Return the number of nodes in a tree"""

    def f(label, folded_subtrees: int):
        return 1 + folded_subtrees

    def g(folded_first: int, folded_rest: int) -> int:
        return folded_first + folded_rest

    return foldtree(f, g, 0, t)


def tree_depth(t: Tuple) -> int:

    def f(label: Any, folded_subtrees: int):
        return 1 + folded_subtrees

    def g(folded_first: int, folded_rest: int) -> int:
        return max(folded_first, folded_rest)

    return foldtree(f, g, 0, t)
