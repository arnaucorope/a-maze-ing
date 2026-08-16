PYTHON = python3
VENV = .venv
BIN = $(VENV)/bin

install:
	$(PYTHON) -m venv $(VENV)
	$(BIN)/pip install -r requirements.txt

build:
	$(BIN)/python -m build
	cp dist/mazegen-1.0.0.tar.gz .

run:
	$(BIN)/python a_maze_ing.py config.txt

debug:
	$(BIN)/python -m pdb a_maze_ing.py config.txt

clean:
	rm -rf mazegen.egg-info
	rm -rf $(VENV)
	rm -rf dist
	rm -rf build
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	rm -f output_maze.txt

lint:
	$(BIN)/flake8 . --exclude=.venv,build,dist
	$(BIN)/mypy . --warn-return-any --warn-unused-ignores \
	--ignore-missing-imports --disallow-untyped-defs \
	--check-untyped-defs
