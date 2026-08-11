import os
import time
from mazegen import Wall
from app.renderer import TerminalRenderer
from mazegen.maze_generator import MazeGenerator
import config_parsing
import sys


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py config.txt")
        return
    
    print("\033[2J\033[H", end="")

    try:
        config = config_parsing.config_parser(sys.argv[1])
    except ValueError as e:
        print(f"Configuration error: {e}")
        return

    maze = MazeGenerator(
        config.width,
        config.height,
        config.entry,
        config.exit_,
        config.perfect,
        config.seed,
    )

    renderer = TerminalRenderer()

    solution: list[Wall] = []

    for grid in maze.generate_steps():
        print("\033[H", end="")

        renderer.draw(
            grid,
            maze.entry,
            maze.exit_,
            solution,
            maze.get_pattern_cells(),
        )

        time.sleep(0.05)

    for direction in maze.solution_steps():
        solution.append(direction)

        print("\033[H", end="")

        renderer.draw(
            grid,
            maze.entry,
            maze.exit_,
            solution,
            maze.get_pattern_cells(),
        )

        time.sleep(0.05)


if __name__ == "__main__":
    main()
