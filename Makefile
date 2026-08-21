PYTHON = python3
VENV = .venv
BIN = $(VENV)/bin

OUTPUT_FILE := $(shell grep '^OUTPUT_FILE=' config.txt | cut -d '=' -f2)

run: install
	$(BIN)/python a_maze_ing.py config.txt

install:
	$(PYTHON) -m venv $(VENV)
	$(BIN)/pip install -r requirements.txt

build:
	$(BIN)/python -m build
	cp dist/mazegen-1.0.0.tar.gz .


debug:
	$(BIN)/python -m pdb a_maze_ing.py config.txt

clean:
	rm -rf mazegen.egg-info
	rm -rf $(VENV)
	rm -rf dist
	rm -rf build
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	rm -f "$(OUTPUT_FILE)"

lint:
	$(BIN)/flake8 . --exclude=.venv,build,dist
	$(BIN)/mypy . --warn-return-any --warn-unused-ignores \
	--ignore-missing-imports --disallow-untyped-defs \
	--check-untyped-defs

anal:
	$(BIN)/python maze_analyzer.py "$(OUTPUT_FILE)"
.PHONY: install run debug clean lint
