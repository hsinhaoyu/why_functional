tangle: org/*.org
	./tangle.sh org/foldtree.org
	./tangle.sh org/newton.org
	./tangle.sh org/diff.org
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
