from abc import ABC, abstractmethod
import random
from .wall import Wall
from collections.abc import Iterator
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .maze_generator import MazeGenerator


class MazeAlgorithm(ABC):
    """Define the interface for maze generation algorithms."""
    @abstractmethod
    def generate(self, maze: "MazeGenerator") -> Iterator[list[list[int]]]:
        pass


class DFSAlgorithm(MazeAlgorithm):
    """Generate mazes using the Depth-First Search algorithm."""

    def generate(self, maze: "MazeGenerator") -> Iterator[list[list[int]]]:
        """Generate a maze using depth-first search.

        The algorithm explores one path as far as possible before
        backtracking to the previous cell.

        Args:
            maze: MazeGenerator instance containing the maze state.

        Yields:
            The current maze grid after each wall is opened.

        Raises:
            RuntimeError: If some reachable cells remain unvisited.
        """
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

                # Yield the grid so the caller can display
                # the current state of the maze.
                yield maze._grid
            else:
                # No unvisited neighbours remain, so backtrack
                # to the previous cell.
                stack.pop()
        expected_cells = (maze.width * maze.height - len(maze._pattern_cells))
        if len(visited) != expected_cells:
            raise RuntimeError("Maze generation left unreachable cells")


class PrimAlgorithm(MazeAlgorithm):
    """Generate mazes using Prim's algorithm."""

    def generate(self, maze: "MazeGenerator") -> Iterator[list[list[int]]]:
        """Generate a maze using a randomized Prim's algorithm.

        The algorithm keeps a frontier of possible connections
        between visited and unvisited cells and randomly selects
        one at each step.

        Args:
            maze: MazeGenerator instance containing the maze state.

        Yields:
            The current maze grid after each wall is opened.

        Raises:
            RuntimeError: If some reachable cells remain unvisited.
        """
        rng = random.Random(maze.seed)
        visited: set[tuple[int, int]] = set()
        frontier: list[
                tuple[
                    tuple[int, int],
                    Wall,
                    tuple[int, int],
                    ]
                ] = []
        start = (0, 0)
        visited.add(start)
        start_x, start_y = start
        neighbours = maze._get_neighbours(start_x, start_y)

        # Add the starting cell's valid neighbours to
        # the frontier.
        for direction, neighbour in neighbours:
            if neighbour not in maze._pattern_cells:
                frontier.append((start, direction, neighbour))
        while frontier:
            option = rng.choice(frontier)
            frontier.remove(option)
            current, direction, neighbour = option

            # Ignore frontier connections leading to cells
            # that have already been visited.
            if neighbour in visited:
                continue
            maze._open_wall(current, direction, neighbour)
            visited.add(neighbour)
            neighbour_x, neighbour_y = neighbour
            new_neighbours = maze._get_neighbours(neighbour_x, neighbour_y)

            # Add the new cell's unvisited neighbours
            # to the frontier.
            for new_direction, new_neighbour in new_neighbours:
                if (
                        new_neighbour not in visited
                        and new_neighbour not in maze._pattern_cells
                        ):
                    frontier.append((neighbour, new_direction, new_neighbour))

            # Yield the grid so the caller can display
            # the current state of the maze.
            yield maze._grid

        expected_cells = (maze.width * maze.height - len(maze._pattern_cells))
        if len(visited) != expected_cells:
            raise RuntimeError("Maze generation left unreachable cells")
