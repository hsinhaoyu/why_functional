[Why Functional Programming Matters](https://www.cs.kent.ac.uk/people/staff/dat/miranda/whyfp90.pdf) is a classic programing article by John Hughes in 1990.

The original code was written in the high-level functional language [Miranda](https://en.wikipedia.org/wiki/Miranda_(programming_language)). I decided to implement the examples in Python. The Python versions are not as elegant as the original, but 

The code is written using `org-babel`, a literate programming tool that comes with Emacs. The documents (`*.org`) can be viewed directly in Github. The Python code under `src/` was extracted from the  `.org` files with Emacs' `M-x org-babel-tangle` command. Or, `make tangle`.
