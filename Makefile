tangle: *.org
	./tangle.sh *.org

lint: tangle
	flake8 --ignore F405,F403,E302 src/

typing: tangle
	mypy --pretty src/*.py

test: tangle
	pytest -s src/

all: tangle lint typing test
