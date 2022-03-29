## Introduction

[Why Functional Programming Matters](https://www.cs.kent.ac.uk/people/staff/dat/miranda/whyfp90.pdf) is a classic programming paper by John Hughes. It's a highly readable and fun introduction to some of the most useful techniques in functional programming. When the paper was published in 1990, the concepts covered were very advanced. Hughes had to use a Haskell-like, high-level functional language [Miranda](https://en.wikipedia.org/wiki/Miranda_(programming_language)) to make his points. 

In recent years, features such as higher-order functions and lazy evaluation have become available in mainstream languages such as Python. However, it still takes some brain-rewiring to take advantage of these abstract constructs. I decided to translate Hughes' Miranda code to Python, as an exercise to become more fluent in functional thinking. Since 90% of Hughes' paper is about lazy evaluation, this is basically an intermediate-level tutorial on Python's generators.

It should be noted that Python's generator really is a poor-person's version of lazy evaluation. A lot of the elegance of the original code was unfortunately lost in translation (at least in my best effort). However, Hughes' main argument - that higher-order functions combined with lazy evaluation allow programmers to decompose densely-linked logic into modular components - remains wise.

## The examples

I embedded the Python code in a series of "articles" that should be read in the following order:

- [Working with trees using higer-order functions](org/foldtree.org)
- [Numerical approximation using lazy evaluation](org/newton.org)
- [Numerican differentiation using iterators of iterators](org/diff.org)
- [Numerical integration using lazy recursion](org/integration.org)
- [Lazy trees](org/lazy_tree.org)
- [Playing games using lazy trees](org/game.org)
- [Playing Tic-tac-toe](org/tic_tac_toe.org)

The code was written in [orgmode](https://orgmode.org) - a markup language with a lightweight literate programming system. It's popular with Emacs users. `orgmode` documents (`*.org`) can be viewed directly in Github. The code blocks in the documents can be extracted (or "tangled" in the jargon of literate programming) into Python code under `src/` with the `M-x org-babel-tangle` command in Emacs. `make tangle` defined in the `Makefile` also does the trick. The source code assembled by `orgmode` doesn't quite follow Python's PEP 8 style guideline, so I use `yapf` to reformat them.
