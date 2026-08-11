import random
from collections import deque
from .wall import Wall
from .algorithms import MazeAlgorithm, DFSAlgorithm, PrimAlgorithm
from collections.abc import Iterator


class MazeGenerator:
    """Generate and manage a maze using the selected algorithm."""
    def __init__(
        self,
        width: int,
        height: int,
        entry: tuple[int, int],
        exit_: tuple[int, int],
        perfect: bool,
        seed: int | None = None,
        algorithm: str = "dfs",
    ) -> None:
        self.width = width
        self.height = height
        self.entry = entry
        self.exit_ = exit_
        self.perfect = perfect
        self.seed = seed
        self.algorithm = algorithm
        self._grid = self._create_grid()
        self._pattern_cells: set[tuple[int, int]] = set()
        self._solution: list[Wall] = []

    def _create_grid(self) -> list[list[int]]:
        grid: list[list[int]] = []

        for _ in range(self.height):
            row: list[int] = []
            for _ in range(self.width):
                row.append(15)
            grid.append(row)

        return grid

    def _is_inside(self, x: int, y: int) -> bool:
        return (
                0 <= x < self.width
                and 0 <= y < self.height
                )

    def _get_neighbours(
            self,
            x: int,
            y: int,
            ) -> list[tuple[Wall, tuple[int, int]]]:
        """Return valid neighbouring cells and their directions."""
        cardinal_directions: list[tuple[Wall, int, int]] = [
                (Wall.NORTH, x, y - 1),
                (Wall.EAST, x + 1, y),
                (Wall.SOUTH, x, y + 1),
                (Wall.WEST, x - 1, y),
                ]
        neighbours: list[tuple[Wall, tuple[int, int]]] = []

        for direction, neighbour_x, neighbour_y in cardinal_directions:
            if self._is_inside(neighbour_x, neighbour_y):
                neighbours.append((direction, (neighbour_x, neighbour_y)))

        return neighbours

    def _is_open_3x3(self, start_x: int, start_y: int) -> bool:
        for y in range(start_y, start_y + 3):
            for x in range(start_x, start_x + 2):
                if self._grid[y][x] & int(Wall.EAST):
                    return False
        for x in range(start_x, start_x + 3):
            for y in range(start_y, start_y + 2):
                if self._grid[y][x] & int(Wall.SOUTH):
                    return False

        return True

    def _would_create_open_3x3(
            self,
            current: tuple[int, int],
            direction: Wall,
            neighbour: tuple[int, int],
            ) -> bool:
        current_x, current_y = current
        neighbour_x, neighbour_y = neighbour
        current_value = self._grid[current_y][current_x]
        neighbour_value = self._grid[neighbour_y][neighbour_x]

        self._open_wall(current, direction, neighbour)
        creates_open_3x3 = False

        for start_y in range(self.height - 2):
            for start_x in range(self.width - 2):
                if self._is_open_3x3(start_x, start_y):
                    creates_open_3x3 = True
                    break
            if creates_open_3x3:
                break
        self._grid[current_y][current_x] = current_value
        self._grid[neighbour_y][neighbour_x] = neighbour_value

        return creates_open_3x3

    def _open_wall(
            self,
            current: tuple[int, int],
            direction: Wall,
            neighbour: tuple[int, int],
            ) -> None:
        current_x, current_y = current
        neighbour_x, neighbour_y = neighbour

        self._grid[current_y][current_x] &= ~int(direction)
        self._grid[neighbour_y][neighbour_x] &= ~int(direction.opposite())

    def _create_42_pattern(self) -> set[tuple[int, int]]:
        pattern: list[list[int]] = [
            [1, 0, 0, 0, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 0, 1, 1, 1],
            [0, 0, 1, 0, 1, 0, 0],
            [0, 0, 1, 0, 1, 1, 1],
            ]

        pattern_height = len(pattern)
        pattern_width = len(pattern[0])
        if (
                self.width < pattern_width + 2
                or self.height < pattern_height + 2
                ):
            print("Error: maze too small for 42 pattern")
            return set()
        start_x = (self.width - pattern_width) // 2
        start_y = (self.height - pattern_height) // 2

        pattern_cells: set[tuple[int, int]] = set()
        for y, row in enumerate(pattern):
            for x, value in enumerate(row):
                if value == 1:
                    pattern_cells.add((start_x + x, start_y + y))
        return pattern_cells

    def _add_extra_passages(self) -> Iterator[list[list[int]]]:
        rng = random.Random(self.seed)

        for y in range(self.height):
            for x in range(self.width):
                current = (x, y)
                if current in self._pattern_cells:
                    continue
                if self._count_open_passages(x, y) != 1:
                    continue
                neighbours = self._get_neighbours(x, y)
                valid_neighbours: list[tuple[Wall, tuple[int, int]]] = []
                for direction, coordinates in neighbours:
                    if coordinates not in self._pattern_cells:
                        valid_neighbours.append((direction, coordinates))
                closed_neighbours: list[tuple[Wall, tuple[int, int]]] = []
                for direction, coordinates in valid_neighbours:
                    if self._grid[y][x] & int(direction):
                        closed_neighbours.append((direction, coordinates))
                if closed_neighbours:
                    rng.shuffle(closed_neighbours)
                    for direction, neighbour in closed_neighbours:
                        if not self._would_create_open_3x3(
                                current,
                                direction,
                                neighbour,
                                ):
                            self._open_wall(current, direction, neighbour)
                            yield self._grid
                            break

    def _count_open_passages(self, x: int, y: int) -> int:
        open_passages = 0
        neighbours = self._get_neighbours(x, y)

        for direction, _ in neighbours:
            if not (self._grid[y][x] & int(direction)):
                open_passages += 1

        return open_passages

    def _validate_entry_exit(self) -> None:
        entry_x, entry_y = self.entry
        exit_x, exit_y = self.exit_

        if not self._is_inside(entry_x, entry_y):
            raise ValueError("Entry is outside the maze")
        if not self._is_inside(exit_x, exit_y):
            raise ValueError("Exit is outside the maze")
        if self.entry == self.exit_:
            raise ValueError("Entry and exit must be different")
        if (
                self.entry in self._pattern_cells
                or self.exit_ in self._pattern_cells
                ):
            raise ValueError("Entry and exit cannot be inside the 42 pattern")

    def _get_open_neighbours(
            self,
            x: int,
            y: int,
            ) -> list[tuple[Wall, tuple[int, int]]]:
        open_neighbours: list[tuple[Wall, tuple[int, int]]] = []
        neighbours = self._get_neighbours(x, y)

        for direction, coordinates in neighbours:
            if not (self._grid[y][x] & int(direction)):
                open_neighbours.append((direction, coordinates))

        return open_neighbours

    def _solve_bfs(self) -> list[Wall]:
        queue: deque[tuple[int, int]] = deque()
        visited: set[tuple[int, int]] = set()
        parents: dict[
                tuple[int, int],
                tuple[tuple[int, int], Wall]
                ] = {}

        queue.append(self.entry)
        visited.add(self.entry)
        while queue:
            current = queue.popleft()
            if current == self.exit_:
                break
            current_x, current_y = current
            open_neighbours = self._get_open_neighbours(current_x, current_y)
            for direction, neighbour in open_neighbours:
                if neighbour in visited:
                    continue
                visited.add(neighbour)
                parents[neighbour] = (current, direction)
                queue.append(neighbour)
        if self.exit_ not in visited:
            raise RuntimeError("No path found between entry and exit")
        path: list[Wall] = []
        current = self.exit_
        while current != self.entry:
            parent, direction = parents[current]
            path.append(direction)
            current = parent
        path.reverse()
        return path

    def generate_steps(self) -> Iterator[list[list[int]]]:
        """Generate the maze step by step,
        yielding the grid after each change."""
        self._grid = self._create_grid()
        self._pattern_cells = self._create_42_pattern()
        self._validate_entry_exit()
        algorithm: MazeAlgorithm
        yield self._grid

        if self.algorithm == "dfs":
            algorithm = DFSAlgorithm()
        elif self.algorithm == "prim":
            algorithm = PrimAlgorithm()
        else:
            raise ValueError(f"Unknown algorithm: {self.algorithm}")
        algorithm_steps = algorithm.generate(self)
        for grid in algorithm_steps:
            yield grid
        if not self.perfect:
            extra_steps = self._add_extra_passages()
            for grid in extra_steps:
                yield grid
        self._solution = self._solve_bfs()

    def generate(self) -> list[list[int]]:
        for _ in self.generate_steps():
            pass

        return self._grid

    def get_solution(self) -> list[Wall]:
        return self._solution.copy()

    def solution_steps(self) -> Iterator[Wall]:
        for direction in self._solution:
            yield direction
