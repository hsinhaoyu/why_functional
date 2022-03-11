## Introduction

[Why Functional Programming Matters](https://www.cs.kent.ac.uk/people/staff/dat/miranda/whyfp90.pdf) is a classic programming paper by John Hughes in 1990. It's a highly readable and fun introduction to some of the most useful techniques in functional programming. It's one of the few programming articles that I read with great joy. In 1990, the concepts that Hughes talked about were very advanced. He had to use a high-level functional language [Miranda](https://en.wikipedia.org/wiki/Miranda_(programming_language)) to make his point. It's interesting that after a couple of decades, a mainstream language like Python can do everything discussed in the paper. Not as elegantly, perhaps, but I suspect that the author didn't anticipate that an entire generation of future programmers would take lazy evaluation and higher-order functions for granted. I decided to implement his examples as an exercise.

## The examples

Hughes' paper argues that functional languages provide elegant mechanisms for decomposing complex programming logic into reusable components 

- [Higher-order functions for trees](foldtree.org): The paper 

## A note on literate programming

I wrote my Python code in [orgmode](https://orgmode.org) - a markup language with literate programming functions. It's popular among Emacs users. `orgmode` documents (`*.org`) can be viewed directly in Github. The code blocks in the documents can be extracted (or "tangled" in the jargon of literate programming) into Python code under `src/` with the `M-x org-babel-tangle` command in Emacs. `make tangle` defined in the `Makefile` also does the trick. The source code assembled by `orgmode` doesn't quite follow Python's PEP 8 style guideline. I use `yapf` to reformat them.

