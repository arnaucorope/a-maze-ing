from mazegen.wall import Wall
import random

GREEN = "\033[32m"
RED = "\033[31m"
RESET = "\033[0m"
BROWN = "\033[33m"
WHITE = "\033[97m"
CYAN = "\033[38;5;30m"

COLORS = [
    "\033[38;5;23m",
    "\033[38;5;24m",
    "\033[38;5;25m",
    "\033[38;5;30m",
    "\033[38;5;31m",
    "\033[38;5;32m",
    "\033[38;5;37m",
    "\033[38;5;38m",
    "\033[38;5;39m",

    "\033[38;5;52m",
    "\033[38;5;53m",
    "\033[38;5;58m",
    "\033[38;5;59m",
    "\033[38;5;60m",
    "\033[38;5;61m",
    "\033[38;5;67m",
    "\033[38;5;68m",

    "\033[38;5;72m",
    "\033[38;5;73m",
    "\033[38;5;74m",
    "\033[38;5;79m",
    "\033[38;5;80m",
    "\033[38;5;81m",
    "\033[38;5;102m",
    "\033[38;5;103m",

    "\033[38;5;108m",
    "\033[38;5;109m",
    "\033[38;5;110m",
    "\033[38;5;116m",
    "\033[38;5;137m",
    "\033[38;5;138m",
    "\033[38;5;139m",
    "\033[38;5;144m",

    "\033[38;5;145m",
    "\033[38;5;146m",
    "\033[38;5;167m",
    "\033[38;5;168m",
    "\033[38;5;173m",
    "\033[38;5;174m",
    "\033[38;5;175m",
    "\033[38;5;180m",
]


class TerminalRenderer:
    """Render the maze and its elements in the terminal.

    Handles the visual representation of walls, the 42 pattern,
    entry, exit, and solution path using terminal colors.
    """

    def __init__(self) -> None:
        self.space = "   "
        self.entry_char = f"{GREEN}███{RESET}"
        self.exit_char = f"{RED}███{RESET}"
        self.solution_char = f"{BROWN}███{RESET}"
        self.wall = f"{WHITE}███{RESET}"
        self.pattern_42 = f"{CYAN}███{RESET}"

    def _create_display_grid(
        self,
        grid: list[list[int]],
    ) -> list[list[str]]:
        """Create an empty display grid based on the maze size.

        Args:
            grid: Maze grid used to determine the display dimensions.

        Returns:
            An empty grid ready to be rendered.
        """

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

    def change_colors(self) -> None:
        """Change the colours of the walls and 42 pattern."""
        wall_color = random.randrange(len(COLORS))
        pattern_color = random.randrange(len(COLORS))

        while pattern_color == wall_color:
            pattern_color = random.randrange(len(COLORS))

        self.wall = f"{COLORS[wall_color]}███{RESET}"
        self.pattern_42 = f"{COLORS[pattern_color]}███{RESET}"

    def _draw_walls(
        self,
        display_grid: list[list[str]],
        grid: list[list[int]],
        pattern_42: set[tuple[int, int]],
    ) -> None:
        """Draw each closed wall according to the cell bitmask."""
        for y in range(len(grid)):
            for x in range(len(grid[y])):
                cell = grid[y][x]

                if (x, y) in pattern_42:
                    wall = self.pattern_42
                else:
                    wall = self.wall

                display_y = y * 2 + 1
                display_x = x * 2 + 1
                if (x, y) in pattern_42:
                    display_grid[display_y][display_x] = self.pattern_42

                display_grid[display_y - 1][display_x - 1] = wall
                display_grid[display_y - 1][display_x + 1] = wall
                display_grid[display_y + 1][display_x - 1] = wall
                display_grid[display_y + 1][display_x + 1] = wall

                if cell & int(Wall.NORTH):
                    display_grid[display_y - 1][display_x] = wall

                if cell & int(Wall.EAST):
                    display_grid[display_y][display_x + 1] = wall

                if cell & int(Wall.SOUTH):
                    display_grid[display_y + 1][display_x] = wall

                if cell & int(Wall.WEST):
                    display_grid[display_y][display_x - 1] = wall

    def _draw_entry_exit(
        self,
        display_grid: list[list[str]],
        entry: tuple[int, int],
        exit_: tuple[int, int],
    ) -> None:
        entry_x, entry_y = entry
        exit_x, exit_y = exit_

        display_grid[entry_y * 2 + 1][entry_x * 2 + 1] = (
            self.entry_char
        )
        display_grid[exit_y * 2 + 1][exit_x * 2 + 1] = (
            self.exit_char
        )

    def _draw_solution(
            self,
            display_grid: list[list[str]],
            entry: tuple[int, int],
            solution: list[Wall],
            ) -> None:
        x, y = entry

        for direction in solution:
            display_y = y * 2 + 1
            display_x = x * 2 + 1

            if direction == Wall.NORTH:
                display_grid[display_y - 1][display_x] = self.solution_char
                y -= 1
            elif direction == Wall.EAST:
                display_grid[display_y][display_x + 1] = self.solution_char
                x += 1
            elif direction == Wall.SOUTH:
                display_grid[display_y + 1][display_x] = self.solution_char
                y += 1
            elif direction == Wall.WEST:
                display_grid[display_y][display_x - 1] = self.solution_char
                x -= 1

            display_y = y * 2 + 1
            display_x = x * 2 + 1
            display_grid[display_y][display_x] = self.solution_char

    def draw(
        self,
        grid: list[list[int]],
        entry: tuple[int, int],
        exit_: tuple[int, int],
        solution: list[Wall],
        pattern_42: set[tuple[int, int]],
    ) -> None:
        """Render walls, solution, entry, and exit,
        then print the complete maze frame."""
        display_grid = self._create_display_grid(grid)

        self._draw_walls(display_grid, grid, pattern_42)
        self._draw_solution(display_grid, entry, solution)
        self._draw_entry_exit(display_grid, entry, exit_)

        for row in display_grid:
            print("".join(row))
