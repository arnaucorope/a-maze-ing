PYTHON = python3
VENV = .venv
BIN = $(VENV)/bin

install:
	$(PYTHON) -m venv $(VENV)
	$(BIN)/pip install -r requirements.txt

build: install
	$(BIN)/python -m build

run: install
	$(BIN)/python a_maze_ing.py config.txt

debug: install
	$(BIN)/python -m pdb a_maze_ing.py config.txt

clean:
	rm output_maze.txt
	rm -rf mazegen.egg-info
	rm -rf $(VENV)
	rm -rf dist
	rm -rf build
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +

lint: install
	$(BIN)/flake8 .
	$(BIN)/mypy . --warn-return-any --warn-unused-ignores \
	--ignore-missing-imports --disallow-untyped-defs \
	--check-untyped-defs
