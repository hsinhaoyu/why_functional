[Why Functional Programming Matters](https://www.cs.kent.ac.uk/people/staff/dat/miranda/whyfp90.pdf) is a classic programming paper by John Hughes in 1990.

The examples in the paper were written in the high-level functional language [Miranda](https://en.wikipedia.org/wiki/Miranda_(programming_language)). I decided to implement the examples in Python. The Python versions are not as elegant as the original, but it's a good exercise to learn some techniques that I haven't used much in my Python programming.

I wrote my Python code in [orgmode](https://orgmode.org) - a markup language with literate programming functions. It's popular among Emacs users. `orgmode` documents (`*.org`) can be viewed directly in Github. The code blocks in the documents can be extracted (or "tangled" in the jargon of literate programming) into Python code under `src/` with the `M-x org-babel-tangle` command in Emacs. Or, `make tangle` also does the trick. The source code assembled by `orgmode` doesn't quite follow Pythons PEP 8 style guideline. I use `yapf` to reformat them.

