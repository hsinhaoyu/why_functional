[Why Functional Programming Matters](https://www.cs.kent.ac.uk/people/staff/dat/miranda/whyfp90.pdf) is a classic programming paper by John Hughes in 1990.

The examples in paper were written in the high-level functional language [Miranda](https://en.wikipedia.org/wiki/Miranda_(programming_language)). I decided to implement the examples in Python. The Python versions are not as elegant as the original, but it's a good exercise to learn some techniques that I haven't used much in my Python programming.

The code is written using `org-babel`, a literate programming tool that comes with Emacs. The documents (`*.org`) can be viewed directly in Github. The Python code under `src/` was extracted from the  `.org` files with Emacs' `M-x org-babel-tangle` command. Or, `make tangle`.
