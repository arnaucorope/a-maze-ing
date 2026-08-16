*This project has been created as part of the 42 curriculum by acoromin, sayala-c.*

# A-Maze-ing

A terminal-based maze generator, solver, visualizer, and reusable Python package developed as part of the 42 curriculum.

## Table of Contents

* [Description](#description)
* [Features](#features)
* [Project Structure](#project-structure)
* [Instructions](#instructions)
* [Configuration File](#configuration-file)
* [Maze Generation](#maze-generation)
* [Maze Representation and Output Format](#maze-representation-and-output-format)
* [Reusable Code](#reusable-code)
* [Team and Project Management](#team-and-project-management)
* [Tools](#tools)
* [Resources](#resources)
* [License](#license)

## Description

**A-Maze-ing** generates mazes from a configuration file, solves them, displays them directly in the terminal, and exports the result in the format required by the project.

The project was designed around two separate layers:

* **`mazegen`**, a reusable maze-generation package containing the maze model, generation algorithms, wall representation, imperfect-maze logic, and shortest-path solver.
* **The application layer**, responsible for configuration parsing, terminal rendering, animation, interaction, and output-file generation.

Each maze contains a centered **42 pattern** made of blocked cells whenever the requested dimensions are large enough to contain it. If the configured entry or exit falls inside this pattern, it is automatically moved to the nearest valid coordinate.

The final application can generate both perfect and imperfect mazes, switch between two generation algorithms, animate maze construction and path solving, display or hide the shortest path, and change the terminal colors interactively.

## Features

* Perfect maze generation.
* Imperfect maze generation with additional passages.
* Dead-end reduction in imperfect mazes.
* Protection against fully open `3 x 3` areas when adding extra passages.
* Two generation algorithms:

  * randomized Depth-First Search (DFS);
  * randomized Prim's algorithm.
* Reproducible generation through an optional seed.
* Centered `42` pattern integrated into the maze.
* Automatic relocation of entry and exit coordinates when they overlap the `42` pattern.
* Breadth-First Search (BFS) shortest-path solver.
* Step-by-step maze generation using Python generators and `yield`.
* Animated shortest-path display.
* Fixed or animated generation modes.
* ANSI-colored terminal renderer.
* Runtime wall/pattern color rotation.
* "Color gambling" animation mode.
* Hexadecimal maze export.
* Reusable `mazegen` Python package.

## Project Structure

```text
.
├── a_maze_ing.py          # Main interactive application
├── config.txt             # Default maze configuration
├── config_parsing.py      # Pydantic-based configuration parser
├── mazegen-1.0.0-py3-none-any.whl  # Reusable mazegen package
├── mazegen-1.0.0.tar.gz            # Reusable mazegen source package
├── exporter.py            # Hex grid and solution exporter
├── app/
│   ├── __init__.py
│   ├── menu.py
│   └── renderer.py        # Terminal maze renderer
├── mazegen/
│   ├── __init__.py
│   ├── algorithms.py      # DFS and Prim implementations
│   ├── maze_generator.py  # Maze generation, solving and maze rules
│   └── wall.py            # Wall bit flags
├── Makefile
├── pyproject.toml         # Package/build configuration
├── requirements.txt
└── LICENSE.md
```

## Instructions

### Requirements

* Python **3.10 or newer**.
* `make`.

The Python dependencies are listed in `requirements.txt` and are installed automatically by the Makefile.

### Installation

Create the virtual environment and install the project dependencies:

```bash
make install
```

This creates a local `.venv` directory and installs the required packages.

### Run

The default configuration is stored in `config.txt`.

```bash
make run
```

Equivalent direct execution:

```bash
.venv/bin/python a_maze_ing.py config.txt
```

To use another configuration file:

```bash
.venv/bin/python a_maze_ing.py path/to/config.txt
```

### Interactive controls

Once the application is running, press the corresponding number without needing to press Enter:

| Key | Action                           |
| --- | -------------------------------- |
| `1` | Generate a new fixed maze        |
| `2` | Generate and animate a new maze  |
| `3` | Switch between DFS and Prim      |
| `4` | Show or hide the shortest path   |
| `5` | Rotate wall and `42` colors      |
| `6` | Run the color-gambling animation |
| `7` | Quit                             |

### Other Makefile commands

Build the reusable package:

```bash
make build
```

Run Flake8 and mypy checks:

```bash
make lint
```

Run the application with Python's debugger:

```bash
make debug
```

Remove generated build files, caches, the virtual environment, and generated output:

```bash
make clean
```

## Configuration File

The configuration file uses one `KEY=VALUE` pair per line.

A complete example is:

```text
WIDTH=15
HEIGHT=15
ENTRY=0,0
EXIT=14,14
OUTPUT_FILE=output_maze.txt
PERFECT=False
SEED=42
```

Whitespace around keys, values, and coordinates is accepted. Keys are normalized to uppercase by the parser. Blank lines and comment lines can be used for readability.

### Available fields

| Key           | Required | Format           | Description                                                   |
| ------------- | -------: | ---------------- | ------------------------------------------------------------- |
| `WIDTH`       |      Yes | positive integer | Number of maze columns                                        |
| `HEIGHT`      |      Yes | positive integer | Number of maze rows                                           |
| `ENTRY`       |      Yes | `x,y`            | Entry coordinate inside maze bounds                           |
| `EXIT`        |      Yes | `x,y`            | Exit coordinate inside maze bounds and different from `ENTRY` |
| `OUTPUT_FILE` |      Yes | non-empty string | Name of the exported maze file                                |
| `PERFECT`     |      Yes | `True` / `False` | Selects perfect or imperfect maze generation                  |
| `SEED`        |       No | integer          | Makes random generation reproducible                          |

The parser is implemented with **Pydantic**. It validates positive dimensions, coordinate syntax, coordinate bounds, different entry/exit positions, the output filename, the perfect-maze flag, and the optional seed.

If the maze is large enough to contain the centered `42` pattern and `ENTRY` or `EXIT` falls on one of its blocked cells, the coordinate is moved automatically to the nearest available cell. Distance is measured using Manhattan distance.

If the maze is too small to contain the pattern, generation continues without it and the renderer displays a warning.

## Maze Generation

### Primary algorithm: randomized Depth-First Search

The primary generation algorithm is a randomized **Depth-First Search**, commonly known in maze generation as the recursive-backtracker approach. Our implementation is iterative and uses an explicit stack instead of Python recursion.

Generation starts from a cell, repeatedly chooses a random unvisited valid neighbour, removes the wall between both cells, and pushes the neighbour onto the stack. When the current cell has no unvisited neighbours, the algorithm backtracks by popping the stack.

Cells belonging to the `42` pattern are excluded from the traversal.

### Why DFS was chosen

DFS was selected as the main algorithm because it offers several useful properties for this project:

* it naturally generates a **perfect maze** when every accessible cell is visited exactly once through the spanning tree;
* its stack-based logic is compact and easy to validate;
* it works naturally with a seeded pseudo-random generator;
* every wall removal is an independent generation step, making it particularly suitable for `yield`-based animation;
* it provides a good base maze that can later be transformed into an imperfect maze.

### Alternative algorithm: randomized Prim

As an advanced feature, the project also implements **randomized Prim's algorithm** behind the same `MazeAlgorithm` interface.

Prim maintains a frontier of candidate edges between visited and unvisited cells. A random frontier edge is selected, and if it reaches an unvisited cell, the corresponding wall is opened and the new cell contributes its own frontier edges.

This produces a different maze topology while keeping the rest of the generator, renderer, solver, and exporter unchanged. The algorithm can be switched directly from the interactive menu.

### Perfect and imperfect mazes

With `PERFECT=True`, the generated maze remains a spanning tree: accessible cells are connected without cycles, so there is exactly one route between any pair of connected cells.

With `PERFECT=False`, the generator starts from the generated perfect maze and opens additional walls around dead ends. Before opening a candidate wall, it checks that the change will not create a completely open `3 x 3` area. These extra passages introduce cycles and reduce dead ends while preserving the `42` pattern.

### Step-by-step generation and animation

`MazeGenerator.generate_steps()` is implemented as a generator. It yields the current grid after each structural change instead of waiting until the whole maze has been generated.

The terminal application consumes these yielded states to redraw the maze frame by frame. The same idea is used by `solution_steps()` to animate the final solution one movement at a time.

A non-animated caller can simply use `generate()`, which consumes all generation steps internally and returns the final grid.

### Shortest path

After maze generation, the project solves the maze using **Breadth-First Search (BFS)**.

BFS explores open neighbours level by level and stores each cell's parent and the direction used to reach it. Once the exit is reached, the path is reconstructed backwards and reversed. Because BFS explores by distance, the returned route is a shortest path from entry to exit, including in imperfect mazes containing cycles.

## Maze Representation and Output Format

### Wall bitmask

Each cell is stored as an integer bitmask. One bit represents each wall:

| Wall  | Value |
| ----- | ----: |
| North |   `1` |
| East  |   `2` |
| South |   `4` |
| West  |   `8` |

The values are combined using bitwise operations. A newly created cell has value `15` (`0xF`), meaning that all four walls are closed. Opening a passage clears the corresponding bit in the current cell and the opposite bit in its neighbour.

This representation is compact, easy to serialize as hexadecimal, and lets the renderer test each wall efficiently with bitwise operations.

### Exported maze file

The exporter writes:

1. one hexadecimal character per maze cell, with one row per line;
2. one blank line;
3. the final entry coordinate as `x,y`;
4. the final exit coordinate as `x,y`;
5. the shortest path as a sequence of `N`, `E`, `S`, and `W` characters.

The path uses the **final** entry and exit positions, including any automatic relocation required by the `42` pattern.

## Reusable Code

# A-Maze-Ing

### 1. What part of your code is reusable, and how?
The most valuable part of this project is the **core maze engine**, which has been isolated from the execution script and delivered as a pre-compiled source distribution package (`.tar.gz`). 

Any external developer can take this archive file and install it into their independent Python projects. By importing `mazegen`, they can reuse the `MazeGenerator` class to create perfect or imperfect mathematical grids, extract matrix data, or plug it into different custom solvers without rewriting the core algorithms from scratch.

---

### 2. How to Set Up and Install the Library From Scratch

Since the `.tar.gz` package is already pre-built and included in the delivery, an external user only needs to run the following commands to install and test the library:

#### Step 1: Create the Virtual Environment
Run the automated Makefile command to set up a clean, isolated Python virtual environment:
```bash
make install
```
This command creates the .venv/ directory and prepares the environment parameters.
#### Step 2: Activate the Virtual Environment
Before installing the package, enter the newly created virtual environment:
```bash
source .venv/bin/activate
```
> *(Your terminal prompt will now show (.venv) at the beginning, confirming you are safely inside the isolated environment).*

#### Step 3: Install the Pre-built Package via pip

Install the delivered .tar.gz archive directly into your active virtual environment using pip:
```bash
pip install dist/mazegen-0.1.0.tar.gz
```
>  *(Note: Replace mazegen-0.1.0.tar.gz with the exact filename of the tar archive present in your repository).*

---
### 3. Implementation Example (How to use it)
Once the package is installed, create an independent testing file named main.py and paste the following clean code inside it:

```python
from mazegen import MazeGenerator

def main():
    maze = MazeGenerator(10, 10, (0, 0), (9, 9), True, "42")
    maze.generate()

    with open("output_maze.txt", "w") as f:
        f.write("\n".join("".join(f"{cell:X}" for cell in row) for row in maze._grid) + "\n")

if __name__ == "__main__":
    main()
```         
#### Run the test script:
To trigger the generator and write the final file, execute:
```bash
python3 main.py
```
You can check that the file output_maze.txt has been successfully created with the hexadecimal grid matrix by running:
```bash
cat output_maze.txt
```

## Team and Project Management

### Team roles

#### acoromin — Maze generation and core logic

Main responsibilities:

* architecture and implementation of the reusable `mazegen` package;
* maze grid and wall-bitmask representation;
* generation algorithms and algorithm abstraction;
* perfect/imperfect maze behavior;
* dead-end reduction and `3 x 3` open-area protection;
* generator-based generation with `yield` for animation;
* BFS solution integration;
* part of the terminal renderer;
* maze exporter and output-format logic.

#### sayala-c — Configuration, application, and visualization

Main responsibilities:

* configuration-file parsing and validation with Pydantic;
* validation of dimensions, coordinates, flags, and seed;
* automatic relocation of entry/exit coordinates when they overlap the `42` pattern;
* a large part of the terminal renderer;
* ANSI colors, color rotation, and color-gambling mode;
* `a_maze_ing.py`, terminal interaction, and menu behavior;
* application-level integration between parser, generator, renderer, and exporter.

#### Shared work

Both team members collaborated on:

* project architecture and integration decisions;
* `pyproject.toml` and package/build setup;
* Makefile targets;
* `requirements.txt`;
* license setup;
* documentation and README;
* final integration, manual testing, and cleanup.

### Initial planning

The initial plan was to divide the project into clear modules and ownership areas:

1. build and validate the core maze representation;
2. implement one reliable generation algorithm first;
3. parse the configuration independently from generation;
4. connect the generator to a basic renderer and exporter;
5. integrate everything through the main application;
6. add optional/advanced features only once the base project was stable.

The main ownership split was between **maze-generation/core logic** and **configuration/application logic**, with integration points agreed between both members.

### How the planning evolved

The project grew beyond the minimum implementation as the base modules became stable.

The generator evolved from a fixed maze-generation flow into an algorithm abstraction supporting both DFS and Prim. Generation was then converted into a generator-based process so the same core logic could power animated and non-animated execution. Imperfect-maze handling was extended to reduce dead ends while preventing completely open `3 x 3` zones.

At the application level, the renderer progressed from a basic wall display to entry/exit rendering, solution visualization, the colored `42` pattern, runtime color changes, and animation. Configuration validation was also expanded so invalid entry/exit positions caused by the central pattern could be corrected automatically rather than simply failing.

The final phase focused on integrating the package, parser, renderer, exporter, terminal controls, build configuration, linting tools, and documentation.

### What worked well

* Keeping `mazegen` independent from the UI made the core code easier to reason about and reuse.
* Dividing responsibilities by module allowed both team members to work in parallel.
* A small interface between generator and renderer (`grid`, entry/exit, solution, pattern cells) reduced coupling.
* Using `yield` allowed animation to be added without duplicating the generation algorithms.
* A common algorithm interface made adding Prim possible without changing the application architecture.
* Regular integration between modules helped expose edge cases involving the `42` pattern, entry/exit positions, and rendering.

### What could be improved

* Automated tests could have been introduced earlier and expanded alongside each feature instead of relying heavily on integration and manual terminal testing.
* Interface contracts between configuration, generation, rendering, and exporting could have been documented earlier to reduce integration adjustments.
* More frequent end-to-end checks of configuration values through to the final exported file would have helped catch inconsistencies sooner.
* Development/prototype files could be cleaned up earlier as functionality moves into its final module.

## Tools

The project used the following tools and libraries:

* **Python 3.10+** — implementation language.
* **Pydantic** — typed configuration validation.
* **Python `random`** — seeded randomized maze generation.
* **Python generators / `yield`** — generation and solution animation.
* **`collections.deque`** — efficient BFS queue.
* **`enum.IntFlag`** — wall bitmask representation.
* **ANSI escape sequences**, `termios`, and `tty` — interactive terminal UI, colors, cursor/screen control, and single-key input.
* **venv** — isolated Python environment.
* **setuptools** and **build** — reusable `mazegen` package build.
* **Make** — common development commands.
* **Flake8** — style/lint checks.
* **mypy** — static type checking.
* **Git** — source control and team collaboration.

## Resources

### Technical references

* Python documentation — `random`: https://docs.python.org/3/library/random.html
* Python documentation — `enum.IntFlag`: https://docs.python.org/3/library/enum.html
* Python documentation — `collections.deque`: https://docs.python.org/3/library/collections.html#collections.deque
* Python language reference — `yield` expressions: https://docs.python.org/3/reference/expressions.html#yield-expressions
* Pydantic documentation — validators: https://docs.pydantic.dev/latest/concepts/validators/
* Python Packaging User Guide: https://packaging.python.org/en/latest/tutorials/packaging-projects/
* Depth-First Search overview: https://en.wikipedia.org/wiki/Depth-first_search
* Prim's algorithm overview: https://en.wikipedia.org/wiki/Prim%27s_algorithm
* Jamis Buck, *Mazes for Programmers*: https://pragprog.com/titles/jbmaze/mazes-for-programmers/

These resources were used to review the behavior of the Python standard-library features involved, configuration validation, packaging, graph traversal, and the maze-generation techniques implemented in the project.

### Use of AI

AI tools, mainly **ChatGPT**, were used as a learning and review assistant during development. They were used for:

* discussing possible project architecture and module separation;
* clarifying maze-generation concepts, bitmasks, graph traversal, generators, and `yield`;
* reviewing and debugging implementation problems during development;
* discussing edge cases involving dead ends, the `42` pattern, entry/exit positions, and animation;
* brainstorming terminal-rendering and user-interface improvements;
* reviewing code structure and helping identify integration issues;
* assisting with the wording and organization of project documentation, including this README.

AI was used to support understanding and review rather than replace the team's implementation work. The final architecture, code integration, feature decisions, testing, and project validation were performed by the team.

## License

See [`LICENSE.md`](LICENSE.md) for the license associated with this project.

