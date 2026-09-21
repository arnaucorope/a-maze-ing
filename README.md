# A-Maze-ing

A Python maze generator, solver, and terminal visualizer, built around a reusable `mazegen` package.

The application generates perfect or imperfect mazes with randomized DFS or Prim, finds a shortest path with BFS, and exports the grid and solution as text. The terminal interface supports step-by-step generation, solution animation, and interactive colors.

## Quick start

Requires Python 3.10 or newer, `make`, and a Unix-like terminal. The interactive application uses `termios`, `tty`, and ANSI escape sequences.

```bash
make install
make run
```

Dependencies are listed in `requirements.txt` and installed into `.venv`. To load a different configuration:

```bash
.venv/bin/python a_maze_ing.py path/to/config.txt
```

### Terminal controls

Press a number without Enter.

| Key | Action |
| --- | --- |
| `1` | Generate a new maze |
| `2` | Animate maze generation and its solution |
| `3` | Select DFS or Prim for the next generation |
| `4` | Show or hide the shortest path |
| `5` | Rotate wall and pattern colors |
| `6` | Run the color-cycling animation |
| `7` | Quit |

Generating a new maze reloads the configuration and exports the result. Menu options `1` and `2` replace the configured seed with a random value; the initial generation uses the configured seed.

## Configuration

The configuration file contains one `KEY=VALUE` pair per line:

```text
WIDTH=15
HEIGHT=15
ENTRY=0,0
EXIT=14,14
OUTPUT_FILE=output_maze.txt
PERFECT=False
SEED=42
```

| Key | Required | Accepted value |
| --- | --- | --- |
| `WIDTH` | Yes | Integer from 1 to 30 |
| `HEIGHT` | Yes | Integer from 1 to 19 |
| `ENTRY` | Yes | In-bounds coordinate `x,y` |
| `EXIT` | Yes | In-bounds coordinate `x,y`, different from entry |
| `OUTPUT_FILE` | Yes | Non-empty output filename |
| `PERFECT` | Yes | Boolean, such as `True` or `False` |
| `SEED` | No | Integer for reproducible generation |

Keys are case-insensitive. Surrounding whitespace, blank lines, and comment lines beginning with `#` are supported. Unknown or duplicate keys are rejected. Pydantic validates field values and coordinate bounds.

A centered `42` pattern is reserved as blocked cells when the grid is at least 9 columns by 7 rows. Smaller grids are generated without the pattern and display a notice. Entry or exit coordinates that overlap the pattern are moved to the nearest available cell by Manhattan distance, keeping the two positions distinct.

## Implementation

### Core package and application

The core `mazegen` package owns the grid, generation algorithms, pattern placement, and pathfinding. It has no dependency on the terminal interface or configuration parser.

The application connects that core to configuration validation, rendering, keyboard input, and export. This separation allows the same generator to be imported into another Python application.

| Location | Responsibility |
| --- | --- |
| `mazegen/maze_generator.py` | Maze state, generation lifecycle, pattern handling, and BFS solver |
| `mazegen/algorithms.py` | Shared algorithm interface and DFS/Prim implementations |
| `mazegen/wall.py` | Wall directions represented with `IntFlag` |
| `config_parsing.py` | Configuration parsing and Pydantic validation |
| `app/renderer.py` | Terminal rendering and colors |
| `a_maze_ing.py` | Interactive menu, animation, and application integration |
| `exporter.py` | Hexadecimal grid and solution export |

### Generation algorithms

**Randomized DFS** uses an explicit stack. It opens a wall to a randomly selected unvisited neighbor and backtracks when no unvisited neighbor remains. This avoids Python recursion and makes each wall removal a natural animation step.

**Randomized Prim** keeps a frontier of candidate edges. It selects an edge at random, opens it if the destination is unvisited, and adds the new cell's frontier edges.

Both algorithms implement the same `MazeAlgorithm` interface and exclude pattern cells. Each verifies that all non-pattern cells were visited.

In perfect mode, generation produces a spanning tree with one path between any two accessible cells. In imperfect mode, an additional pass opens walls around dead ends, introducing cycles. Candidate openings are rejected if they would create a completely open `3 × 3` area. This reduces dead ends without guaranteeing their removal in every configuration.

### Step-by-step execution and pathfinding

`generate_steps()` yields the current grid as walls are opened. The terminal application redraws each state; `generate()` consumes the same steps internally and returns the completed grid. Yielded grids reference the mutable grid, so callers retaining past frames must copy them.

The solver uses BFS with a `deque` and records each visited cell's parent and incoming direction. It reconstructs the route from exit to entry and reverses it. Since each passage has equal cost, this finds a shortest path even when the maze contains cycles.

### Grid representation and export

Each cell stores four wall bits:

| Wall | Value |
| --- | ---: |
| North | `1` |
| East | `2` |
| South | `4` |
| West | `8` |

A cell starts at `15` (`0xF`), with all walls closed. Opening a passage clears the appropriate bit in both neighboring cells. Coordinates use `(x, y)`; grid access uses `grid[y][x]`.

The exported file contains:

1. One hexadecimal character per cell, with one grid row per line.
2. A blank line.
3. The final entry coordinate as `x,y`.
4. The final exit coordinate as `x,y`.
5. The solution as a sequence of `N`, `E`, `S`, and `W`.

Export uses the final coordinates after any pattern-related relocation.

## Using the package

To install the included source distribution into a virtual environment:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install ./mazegen-1.0.0.tar.gz
```

The core can then be used independently:

```python
from mazegen import MazeGenerator

maze = MazeGenerator(
    width=15,
    height=15,
    entry=(0, 0),
    exit_=(14, 14),
    perfect=False,
    seed=42,
    algorithm="prim",
)

grid = maze.generate()
solution = maze.get_solution()
```

`generate()` returns a two-dimensional list of wall masks. `get_solution()` returns a list of `Wall` directions. The `algorithm` parameter accepts `"dfs"` or `"prim"`; DFS is the default.

The Pydantic configuration checks belong to the application layer. Callers using `MazeGenerator` directly are responsible for supplying valid dimensions and coordinates.

See the [package README](mazegen/README.md) for additional usage examples.

## Development commands

Run `make install` before commands that use the virtual environment.

| Command | Purpose |
| --- | --- |
| `make build` | Build distributions in `dist/` and copy the source archive to the repository root |
| `make lint` | Run Flake8 and mypy |
| `make debug` | Start the application with Python's debugger |
| `make clean` | Remove the environment, build artifacts, caches, and configured output file |

## Authors and contributions

Developed jointly by **Arnau Corominas Pérez (acoromin)** and **Sara Ayala (sayala-c)** as part of the 42 curriculum.

- **Arnau Corominas Pérez (acoromin):** reusable package architecture, grid and wall representation, generation algorithms, imperfect-maze logic, generator-based animation, BFS integration, export, and part of the renderer.
- **sayala-c:** configuration parsing and validation, entry/exit relocation, much of the renderer, terminal colors and interaction, and application integration.
- **Shared:** architecture and integration decisions, packaging, Makefile, dependencies, licensing, documentation, and manual testing.

AI tools supported architecture discussions, concept exploration, debugging, integration review, and documentation. Implementation, integration, and validation were performed by the team.

## References and license

Reference material included Python documentation for `random`, `IntFlag`, `deque`, and generators; Pydantic's validation documentation; the Python Packaging User Guide; and Jamis Buck's *Mazes for Programmers*.

See [LICENSE.md](LICENSE.md) for licensing terms.
