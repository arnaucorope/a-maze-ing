import sys
import termios
import time
import tty
import random
from mazegen import Wall
from app.renderer import TerminalRenderer
from mazegen.maze_generator import MazeGenerator
import config_parsing
from exporter import export_grid


def start_screen() -> None:
    """Start the application in an alternate terminal screen.

    The alternate screen keeps the application output separate from
    the user's normal terminal history.
    """
    # Switch to the alternate terminal screen.
    # Everything displayed by the application is kept in this
    # separate screen buffer.
    print("\033[?1049h", end="")

    # Clear the screen and move the cursor to the top-left corner.
    print("\033[2J\033[H", end="")

    # Hide the cursor while the application is running.
    print("\033[?25l", end="")


def end_screen() -> None:
    """Restore the normal terminal screen and show the cursor."""

    # Show the cursor again before leaving the application.
    print("\033[?25h", end="")

    # Leave the alternate screen and restore the normal terminal.
    print("\033[?1049l", end="")


def get_key() -> str:
    """Read one key from the terminal without pressing Enter.
    Returns the character pressed by the user."""

    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)

    try:
        # Raw mode makes the terminal send each key immediately
        # instead of waiting for the Enter key.
        tty.setraw(fd)
        return sys.stdin.read(1)
    finally:
        # Restore the original terminal settings after reading
        # the key so the terminal does not remain in raw mode.
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)


def clear_screen() -> None:
    """Clear the terminal screen and move the cursor to the top-left."""

    # \033[2J clears the screen.
    # \033[H moves the cursor to the top-left corner.
    print("\033[2J\033[H", end="")


def draw_screen(
    maze: MazeGenerator,
    grid: list[list[int]],
    solution: list[Wall],
    show_solution: bool,
    renderer: TerminalRenderer,
) -> None:
    """Draw the maze, warnings, and menu on the terminal.

    Args:
        maze: MazeGenerator containing the current maze information.
        grid: Current maze grid to render.
        solution: List of walls representing the maze solution.
        show_solution: Whether the shortest path should be displayed.
        renderer: Terminal renderer used to display the maze."""
    clear_screen()

    # Only pass the solution to the renderer when it should be visible.
    if show_solution:
        path = solution
    else:
        path = []

    renderer.draw(
        grid,
        maze.entry,
        maze.exit_,
        path,
        maze.get_pattern_cells(),
    )
    # Display an error if the maze is too small for the 42 pattern.
    if not maze.pattern_fits:
        print()
        RED = "\033[31m"
        YELLOW = "\033[33m"
        RESET = "\033[0m"

        print(
                f"{RED}✖ Error:{RESET} "
                f"The maze is too small to fit the {YELLOW}42{RESET} pattern."
            )

    # Display a warning if the configured entry was inside
    # the 42 pattern and had to be moved.
    if maze.entry_moved:
        print()
        print("\033[93mWarning: Entry coordinates were inside "
              "the 42 pattern and have been moved to the "
              f"nearest available coordinate: {maze.entry}\033[0m")

    if maze.exit_moved:
        print()
        print("\033[93mWarning: Exit coordinates were inside "
              "the 42 pattern and have been moved to the "
              f"nearest available coordinate.{maze.exit_}\033[0m")

    print()
    print("=== A-Maze-ing ===")
    print("1. Generate fixed maze")
    print("2. Generate animated maze")
    print(f"3. Change algorithm. Current: {maze.algorithm}")
    print("4. Show/Hide the shortest path")
    print("5. Rotate the wall colours")
    print("6. Color gambling")
    print("7. Quit")
    print()
    print("Press a number (1-7) to select an option: ", end="", flush=True)


def fixed_maze(
    maze: MazeGenerator,
) -> tuple[list[list[int]], list[Wall]]:
    """Generate a complete maze and calculate its solution.

    Args:
        maze: MazeGenerator used to create the maze.

    Returns:
        A tuple containing the generated grid and its solution.
    """

    grid = maze.generate()
    solution = maze.get_solution()

    return grid, solution


def animated_maze(
    maze: MazeGenerator,
    renderer: TerminalRenderer,
) -> tuple[list[list[int]], list[Wall]]:
    """Generate and display the maze and solution step by step.

    Args:
        maze: MazeGenerator used to create the maze.
        renderer: Terminal renderer used to display each generation step.

    Returns:
        A tuple containing the completed grid and its solution.
    """

    solution: list[Wall] = []
    grid: list[list[int]] = []

    # Animate the maze generation by rendering every grid
    # produced by generate_steps().
    for grid in maze.generate_steps():
        clear_screen()

        renderer.draw(
            grid,
            maze.entry,
            maze.exit_,
            solution,
            maze.get_pattern_cells(),
        )

        time.sleep(0.05)

    # Animate the solution by adding one direction at a time
    # and redrawing the maze after each step.
    for direction in maze.solution_steps():
        solution.append(direction)

        clear_screen()

        renderer.draw(
            grid,
            maze.entry,
            maze.exit_,
            solution,
            maze.get_pattern_cells(),
        )

        time.sleep(0.05)

    return grid, solution


def main() -> None:
    """Load the configuration and run the interactive maze menu."""

    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py config.txt")
        return

    try:
        config = config_parsing.config_parser(sys.argv[1])
    except FileNotFoundError:
        print(f"Error: configuration file '{sys.argv[1]}' not found.")
        print("Usage: python3 a_maze_ing.py config.txt")
        return

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

    running = True

    # Enter the alternate screen before starting the interactive
    # application. The normal terminal contents remain untouched.
    start_screen()

    show_solution = True
    dfs = True
    renderer = TerminalRenderer()
    try:
        # Generate the first maze so that the application starts
        # with a maze already displayed.
        grid, solution = fixed_maze(maze)
        export_grid(
            grid,
            maze.entry,
            maze.exit_,
            solution,
            config.output_file
        )

        while running:

            # Redraw the complete screen after every user action.
            # This keeps the maze and menu in the same fixed position.
            draw_screen(
                maze,
                grid,
                solution,
                show_solution,
                renderer,
            )

            # Wait for one key without requiring Enter.
            option = get_key()

            match option:
                case "1":
                    maze.seed = random.randint(1, 100)
                    grid, solution = fixed_maze(maze)
                    export_grid(
                            grid,
                            maze.entry,
                            maze.exit_,
                            solution,
                            config.output_file
                        )
                case "2":
                    maze.seed = random.randint(1, 100)
                    grid, solution = animated_maze(maze, renderer)
                    export_grid(
                            grid,
                            maze.entry,
                            maze.exit_,
                            solution,
                            config.output_file
                        )
                case "3":
                    dfs = not dfs
                    if not dfs:
                        maze.algorithm = "prim"
                    else:
                        maze.algorithm = "dfs"
                case "4":
                    show_solution = not show_solution
                case "5":
                    renderer.change_colors()
                case "6":
                    update = 0.005
                    for i in range(300):
                        renderer.change_colors()
                        draw_screen(
                            maze,
                            grid,
                            solution,
                            show_solution,
                            renderer,
                        )

                        if i > 260:
                            update += 0.005
                            time.sleep(update)
                        else:
                            time.sleep(0.005)
                case "7":
                    running = False

    finally:
        # Always restore the normal terminal, even if an exception
        # occurs while the application is running.
        end_screen()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nProgram interrupted by user.")
