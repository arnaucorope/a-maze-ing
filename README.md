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
* [Bonus Features](#bonus-features)
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
├── a_maze_ing.py              # Main interactive application
├── config.txt                 # Default maze configuration
├── config_parsing.py          # Pydantic-based configuration parser
├── exporter.py                # Hex grid and solution exporter
├── mazegen-1.0.0.tar.gz       # Installable reusable mazegen package
│
├── app/
│   ├── __init__.py
│   └── renderer.py            # Terminal maze renderer
│
├── mazegen/
│   ├── __init__.py
│   ├── algorithms.py          # DFS and Prim implementations
│   ├── maze_generator.py      # Maze generation, solving and maze rules
│   ├── wall.py                # Wall bit flags
│   └── README.md              # Documentation for the reusable package
│
├── .gitignore
├── LICENSE.md
├── Makefile
├── pyproject.toml             # Package/build configuration
├── README.md
└── requirements.txt
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

The reusable component of this project is the **`mazegen` package**, which contains the core maze-generation logic independently from the configuration parser, terminal renderer, exporter, and interactive application.

The package is provided as a source distribution at the root of the repository:

```text
mazegen-1.0.0.tar.gz
```

### Installation

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install the package directly with `pip`:

```bash
python -m pip install ./mazegen-1.0.0.tar.gz
```

Once installed, `MazeGenerator` can be imported from any Python project:

```python
from mazegen import MazeGenerator
```

### Basic usage

```python
from mazegen import MazeGenerator

maze = MazeGenerator(
    width=10,
    height=10,
    entry=(0, 0),
    exit_=(9, 9),
    perfect=False,
    seed=42,
)

grid = maze.generate()

for row in grid:
    print("".join(f"{cell:X}" for cell in row))
```

`generate()` returns the generated maze structure as a two-dimensional list of integers. Each integer represents the walls of one cell using a four-bit wall representation.

The returned grid can therefore be reused directly by another project, such as a Pac-Man-like game, or converted to hexadecimal as shown in the example above.

### Custom parameters

The generator accepts custom parameters including:

| Parameter | Description |
| --- | --- |
| `width` | Number of maze columns |
| `height` | Number of maze rows |
| `entry` | Entry coordinate as `(x, y)` |
| `exit_` | Exit coordinate as `(x, y)` |
| `perfect` | Selects perfect or imperfect maze generation |
| `seed` | Optional seed for reproducible generation |
| `algorithm` | Generation algorithm (`"dfs"` or `"prim"`) |

For example, Prim can be selected with:

```python
maze = MazeGenerator(
    width=20,
    height=15,
    entry=(0, 0),
    exit_=(19, 14),
    perfect=False,
    seed=42,
    algorithm="prim",
)
```

### Rebuilding the package

All elements required to rebuild the reusable package are included in the repository.

Run:

```bash
make build
```

The standard Python build process creates the package distributions inside `dist/`. The source distribution submitted with the project is copied to the repository root as `mazegen-1.0.0.tar.gz`.

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

## Bonus Features

In addition to the mandatory requirements, the project implements several advanced features:

- **Multiple generation algorithms** — the user can switch between randomized DFS and Prim.
- **Animated maze generation** — maze construction can be displayed step by step using Python generators and `yield`.
- **Animated solution path** — the shortest path can also be displayed progressively.
- **Dead-end removal** — imperfect mazes are processed to remove dead ends while preventing fully open `3 x 3` areas.
- **Color gambling** — an animated terminal effect that continuously changes the maze colors.
- **Automatic entry/exit relocation** — if the configured entry or exit overlaps the `42` pattern, it is automatically moved to the nearest valid cell.

## License

See [`LICENSE.md`](LICENSE.md) for the license associated with this project.

