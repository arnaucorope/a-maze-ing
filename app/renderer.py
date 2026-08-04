from mazegen.wall import Wall


class TerminalRenderer:
    def __init__(self) -> None:
        self.wall = "███"
        self.space = "   "
        self.entry_char = " ■ "
        self.exit_char = " ■ "

    def _create_display_grid(self, grid: list[list[int]]) -> list[list[str]]:
        height = len(grid)
        width = len(grid[0])

        display_width = width * 2 + 1
        display_height = height * 2 + 1
        display_grid: list[list[str]] = []

        for _ in range(display_height):
            row: list[str] = []
            for _ in range(display_width):
                row.append(self.space)
            display_grid.append(row)

        return display_grid

    def _draw_walls(
            self, display_grid: list[list[str]], grid: list[list[int]]
            ) -> None:
        for y in range(len(grid)):
            for x in range(len(grid[y])):
                cell = grid[y][x]
                display_y = y * 2 + 1
                display_x = x * 2 + 1

                display_grid[display_y - 1][display_x - 1] = self.wall
                display_grid[display_y - 1][display_x + 1] = self.wall
                display_grid[display_y + 1][display_x - 1] = self.wall
                display_grid[display_y + 1][display_x + 1] = self.wall

                if cell & int(Wall.NORTH):
                    display_grid[display_y - 1][display_x] = self.wall
                if cell & int(Wall.EAST):
                    display_grid[display_y][display_x + 1] = self.wall
                if cell & int(Wall.SOUTH):
                    display_grid[display_y + 1][display_x] = self.wall
                if cell & int(Wall.WEST):
                    display_grid[display_y][display_x - 1] = self.wall

    def _draw_entry_exit(
            self,
            display_grid: list[list[str]],
            entry: tuple[int, int],
            exit_: tuple[int, int],
            ) -> None:
        entry_x, entry_y = entry
        exit_x, exit_y = exit_

        display_grid[entry_y * 2 + 1][entry_x * 2 + 1] = self.entry_char
        display_grid[exit_y * 2 + 1][exit_x * 2 + 1] = self.exit_char

    def draw(
            self,
            grid: list[list[int]],
            entry: tuple[int, int],
            exit_: tuple[int, int],
            ) -> None:
        display_grid = self._create_display_grid(grid)
        self._draw_walls(display_grid, grid)
        self._draw_entry_exit(display_grid, entry, exit_)

        for row in display_grid:
            print("".join(row))
