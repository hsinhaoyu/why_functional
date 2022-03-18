tangle: org/*.org
	# delete all files except zz.py
	find src/ ! -name 'zz.py' -type f -maxdepth 1 -exec rm -f {} +
	./tangle.sh org/foldtree.org
	./tangle.sh org/newton.org
	./tangle.sh org/diff.org
	./tangle.sh org/integration.org
	./tangle.sh org/lazy_tree.org
	./tangle.sh org/tic_tac_toe.org
	yapf --in-place --recursive src/

lint: tangle
	flake8 --ignore F405,F403,E302 src/

typing: tangle
	mypy --pretty src/*.py

test: tangle
	pytest -s src/

html: tangle
	./org2html.sh org/*.org

all: tangle lint typing test html
