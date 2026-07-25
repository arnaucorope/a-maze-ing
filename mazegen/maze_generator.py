class MazeGenerator:
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
            ) -> list[tuple[str, tuple[int, int]]]:
        cardinal_directions: list[tuple[str, int, int]] = [
                ("N", x, y - 1),
                ("E", x + 1, y),
                ("S", x, y + 1),
                ("W", x - 1, y),
                ]
        neighbours: list[tuple[str, tuple[int, int]]] = []

        for direction, neighbour_x, neighbour_y in cardinal_directions:
            if self._is_inside(neighbour_x, neighbour_y):
                neighbours.append((direction, (neighbour_x, neighbour_y)))

        return neighbours
