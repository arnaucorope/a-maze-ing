import os
import time
from mazegen import Wall
from app.renderer import TerminalRenderer
from mazegen.maze_generator import MazeGenerator


def main() -> None:
    maze = MazeGenerator(
        width=11,
        height=11,
        entry=(0, 0),
        exit_=(10, 10),
        perfect=False,
        algorithm="dfs",
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
        )

        time.sleep(0.05)

if __name__ == "__main__":
    main()
