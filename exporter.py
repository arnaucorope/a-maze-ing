from mazegen import Wall


def grid_to_hex(grid: list[list[int]]) -> str:
    """Convert the maze grid into hexadecimal text.

    Args:
        grid: Maze grid represented as integer values.

    Returns:
        The hexadecimal representation of the grid.
    """
    lines: list[str] = []

    for row in grid:
        line = ""

        for cell in row:
            hexadecimal = format(cell, "X")
            line += hexadecimal

        lines.append(line)

    return "\n".join(lines)


def solution_to_text(solution: list[Wall]) -> str:
    """Convert the maze solution into directional text.

    Args:
        solution: List of wall directions forming the solution path.

    Returns:
        The solution represented using N, E, S, and W characters.
    """
    text = ""

    for direction in solution:
        if direction == Wall.NORTH:
            text += "N"
        elif direction == Wall.EAST:
            text += "E"
        elif direction == Wall.SOUTH:
            text += "S"
        elif direction == Wall.WEST:
            text += "W"

    return text


def export_grid(
        grid: list[list[int]],
        entry: tuple[int, int],
        exit_: tuple[int, int],
        solution: list[Wall],
        filename: str,
        ) -> None:
    """Export the maze grid, coordinates, and solution to a file.

    Args:
        grid: Maze grid represented as integer values.
        entry: Entry coordinates of the maze.
        exit_: Exit coordinates of the maze.
        solution: List of wall directions forming the solution path.
        filename: Path of the output file.
    """
    hex_grid = grid_to_hex(grid)
    solution_text = solution_to_text(solution)
    entry_x, entry_y = entry
    exit_x, exit_y = exit_

    try:
        with open(filename, "w", encoding="utf-8") as file:
            file.write(hex_grid)
            file.write("\n\n")
            file.write(f"{entry_x},{entry_y}\n")
            file.write(f"{exit_x},{exit_y}\n")
            file.write(solution_text)
            file.write("\n")
    except OSError as error:
        print(f"Error writing output file: {error}")
