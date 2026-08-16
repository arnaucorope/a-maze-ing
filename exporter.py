from mazegen import Wall


def grid_to_hex(grid: list[list[int]]) -> str:
    lines: list[str] = []

    for row in grid:
        line = ""

        for cell in row:
            hexadecimal = format(cell, "X")
            line += hexadecimal

        lines.append(line)

    return "\n".join(lines)


def solution_to_text(solution: list[Wall]) -> str:
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
