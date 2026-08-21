*Developed by **acoromin** and **sayala-c** as part of the 42 curriculum.*

# mazegen

`mazegen` is the reusable maze-generation package developed for the **A-Maze-ing** project.

It contains the core maze-generation logic independently from the configuration parser, terminal renderer, exporter, and interactive application, so it can be installed and imported into another Python project.

## Installation

The package is distributed as:

```text
mazegen-1.0.0.tar.gz
```

From the directory containing the archive, install it with:

```bash
python -m pip install ./mazegen-1.0.0.tar.gz
```

Using a virtual environment is recommended:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install ./mazegen-1.0.0.tar.gz
```

## Import

Once installed:

```python
from mazegen import MazeGenerator
```

## Basic usage

```python
from mazegen import MazeGenerator


def main() -> None:
    maze = MazeGenerator(
        width=10,
        height=10,
        entry=(0, 0),
        exit_=(9, 9),
        perfect=False,
        seed=42,
    )

    grid = maze.generate()
    solution = maze.get_solution()

    solution_text = "".join(direction.name[0] for direction in solution)

    output = ""

    for row in grid:
        output += "".join(f"{cell:X}" for cell in row) + "\n"

    output += "\n"
    output += f"{maze.entry[0]},{maze.entry[1]}\n"
    output += f"{maze.exit_[0]},{maze.exit_[1]}\n"
    output += solution_text + "\n"

    print(output, end="")

    with open("maze_output.txt", "w", encoding="utf-8") as file:
        file.write(output)


if __name__ == "__main__":
    main()

```

`generate()` returns the generated maze as a two-dimensional list of integers.

Each integer represents the walls of one cell using a four-bit mask:

| Wall | Value |
| --- | ---: |
| North | `1` |
| East | `2` |
| South | `4` |
| West | `8` |

A newly created cell has value `15` (`0xF`), meaning that all four walls are closed.

## Hexadecimal grid

The generated structure can be converted directly to hexadecimal:

```python
for row in grid:
    print("".join(f"{cell:X}" for cell in row))
```

This representation can be reused by another project, for example as the map structure of a Pac-Man-like game.

## Custom parameters

`MazeGenerator` accepts the following parameters:

| Parameter | Description |
| --- | --- |
| `width` | Number of maze columns |
| `height` | Number of maze rows |
| `entry` | Entry coordinate as `(x, y)` |
| `exit_` | Exit coordinate as `(x, y)` |
| `perfect` | `True` for a perfect maze, `False` for an imperfect maze |
| `seed` | Optional seed for reproducible generation |
| `algorithm` | Generation algorithm: `"dfs"` or `"prim"` |

Example using Prim:

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

grid = maze.generate()
```

## Accessing a solution

After generating the maze, a shortest valid path is available with:

```python
solution = maze.get_solution()
```

## Step-by-step generation

For applications that need each generation state, such as animations or custom visualizers:

```python
for grid in maze.generate_steps():
    pass
```

## Authors

Developed by **acoromin** and **sayala-c** as part of the 42 curriculum.
