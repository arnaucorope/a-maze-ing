from abc import ABC, abstractmethod
import random
from .wall import Wall
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .maze_generator import MazeGenerator


class MazeAlgorithm(ABC):
    @abstractmethod
    def generate(self, maze: "MazeGenerator") -> None:
        pass


class DFSAlgorithm(MazeAlgorithm):
    def generate(self, maze: "MazeGenerator") -> None:
        visited: set[tuple[int, int]] = set()
        stack: list[tuple[int, int]] = []
        rng = random.Random(maze.seed)

        start: tuple[int, int] = (0, 0)
        visited.add(start)
        stack.append(start)

        while stack:
            current = stack[-1]
            current_x, current_y = current

            neighbours = maze._get_neighbours(current_x, current_y)
            unvisited_neighbours: list[tuple[Wall, tuple[int, int]]] = []
            for direction, coordinates in neighbours:
                if (
                        coordinates not in visited
                        and coordinates not in maze._pattern_cells
                        ):
                    unvisited_neighbours.append((direction, coordinates))

            if unvisited_neighbours:
                direction, next_cell = rng.choice(unvisited_neighbours)
                maze._open_wall(current, direction, next_cell)
                visited.add(next_cell)
                stack.append(next_cell)
            else:
                stack.pop()
        expected_cells = (maze.width * maze.height - len(maze._pattern_cells))
        if len(visited) != expected_cells:
            raise RuntimeError("Maze generation left unreachable cells")
