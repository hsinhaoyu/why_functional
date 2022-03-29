from typing import Tuple, Callable, Any, List, Union, NamedTuple
import operator

Node = NamedTuple('Node', [('label', Any), ('subtrees', List)])


def foldtree(f: Callable, g: Callable, a: Any, t: Union[Node, List]) -> Any:
    """Apply two functions (f and g) of two arguments to transform a tree.
    f: fold a node's label to the folded subtrees
    g: fold a list of subtrees
    a: an initial constant
    t: a tree, a list of subtrees, or []
    """
    if t == []:
        return a
    elif isinstance(t, Node):
        (label, subtrees) = t
        return f(label, foldtree(f, g, a, subtrees))
    else:
        # fold multiple subtrees
        subtree = t[0]
        rest = t[1:]
        return g(foldtree(f, g, a, subtree), foldtree(f, g, a, rest))


def sumtree(t: Node) -> int:
    """Sum all labels in a tree."""
    f = operator.add
    g = operator.add
    return foldtree(f, g, 0, t)


def tree_labels(t: Node):
    """Collect all labels of a tree into a list."""

    def f(label: Any, folded_subtrees: List) -> List:
        return [label] + folded_subtrees

    def g(folded_first: List, folded_rest: List) -> List:
        return folded_first + folded_rest

    return foldtree(f, g, [], t)


def maptree(func: Callable, t: Node) -> Node:
    """Map a function to all labels in a tree.
    Return a new tree.
    """

    def f(label: Any, folded_subtrees: List) -> Node:
        return Node(func(label), folded_subtrees)

    def g(folded_first: Node, folded_rest: List) -> List:
        return [folded_first] + folded_rest

    return foldtree(f, g, [], t)


def tree_size(t: Node) -> int:
    """Return the number of nodes in a tree"""

    def f(label: int, folded_subtrees: int) -> int:
        return 1 + folded_subtrees

    def g(folded_first: int, folded_rest: int) -> int:
        return folded_first + folded_rest

    return foldtree(f, g, 0, t)


def tree_depth(t: Node) -> int:
    """Returns the maximal depth of nodes in the tree"""

    def f(label: Any, folded_subtrees: int) -> int:
        return 1 + folded_subtrees

    def g(folded_first: int, folded_rest: int) -> int:
        return max(folded_first, folded_rest)

    return foldtree(f, g, 0, t)
