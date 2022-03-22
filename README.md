## Introduction

[Why Functional Programming Matters](https://www.cs.kent.ac.uk/people/staff/dat/miranda/whyfp90.pdf) is a classic programming paper by John Hughes. It's a highly readable and fun introduction to some of the most useful techniques in functional programming. When the paper was published in 1990, the concepts covered were very advanced. Hughes had to use a high-level functional language [Miranda](https://en.wikipedia.org/wiki/Miranda_(programming_language)) to make his points. I suspect that he didn't anticipate that in a couple of decades, an entire generation of future programmers would take lazy evaluation and higher-order functions for granted. I decided to implement his examples in Python as an exercise, because I enjoyed reading it so much. It's interesting that the Python conversions are not nearly as elegant as his original code.

## The examples

Hughes argued that functional languages provide elegant mechanisms for decomposing complex programming logic into reusable components, in a way that is very difficult or impossible with imperative languages. The two most important "glues" are high-order functions and lazy evaluation.

- [Working with trees using higer-order functions](org/foldtree.org)
- [Numerical approximation using lazy evaluation](org/newton.org)
- [Numerican differentiation using iterators of iterators](org/diff.org)
- [Numerical integration using lazy recursion](org/integration.org)
- [Lazy trees](org/lazy_tree.org)
- [Playing Tic-tac-toe using lazy trees](org/tic_tac_toe.org)

## A note on literate programming

I wrote my Python code in [orgmode](https://orgmode.org) - a markup language with literate programming functions. It's popular among Emacs users. `orgmode` documents (`*.org`) can be viewed directly in Github. The code blocks in the documents can be extracted (or "tangled" in the jargon of literate programming) into Python code under `src/` with the `M-x org-babel-tangle` command in Emacs. `make tangle` defined in the `Makefile` also does the trick. The source code assembled by `orgmode` doesn't quite follow Python's PEP 8 style guideline. I use `yapf` to reformat them.

