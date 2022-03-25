tangle: org/*.org
	# delete all files except zz.py
	find src/ ! -name 'zz*.py' -type f -maxdepth 1 -exec rm -f {} +

	./tangle.sh org/foldtree.org
	./tangle.sh org/newton.org
	./tangle.sh org/diff.org
	./tangle.sh org/integration.org
	./tangle.sh org/lazy_tree.org
	./tangle.sh org/game.org
	./tangle.sh org/tic_tac_toe.org
	./tangle.sh org/tests.org
	yapf --in-place --recursive src/

lint: tangle
	flake8 --ignore F403,F405,E266,E302 src/

typing: tangle
	mypy --pretty src/*.py

test: tangle
	pytest -s --cov src/

html: tangle
	./org2html.sh org/*.org

all: tangle lint typing test html

zz:
	./tangle.sh org/tic_tac_toe.org
	python src/zz.py
