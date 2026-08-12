import sys
import termios
import time
import tty
import random
from mazegen import Wall
from app.renderer import TerminalRenderer
from mazegen.maze_generator import MazeGenerator
import config_parsing
import select


def start_screen() -> None:
    """Start the terminal alternate screen."""
    # Entra en una pantalla alternativa.
    # Todo lo que hagamos aquí queda aislado de la terminal normal.
    print("\033[?1049h", end="")

    # Limpia la pantalla y coloca el cursor en 0,0.
    print("\033[2J\033[H", end="")

    # Oculta el cursor.
    print("\033[?25l", end="")


def end_screen() -> None:
    """Restore the normal terminal screen."""
    # Muestra el cursor.
    print("\033[?25h", end="")

    # Vuelve a la pantalla normal.
    print("\033[?1049l", end="")


def get_key() -> str:
    """Read one key without pressing Enter."""
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)

    try:
        tty.setraw(fd)
        return sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)


def clear_screen() -> None:
    """Clear the current screen and move to 0,0."""
    print("\033[2J\033[H", end="")


def draw_screen(
    maze: MazeGenerator,
    grid: list[list[int]],
    solution: list[Wall],
    show_solution: bool,
    renderer: TerminalRenderer,
) -> None:
    """Draw the maze and menu."""
    clear_screen()

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
    if not maze.pattern_fits:
        print()
        RED = "\033[31m"
        YELLOW = "\033[33m"
        RESET = "\033[0m"

        print(
                f"{RED}✖ Error:{RESET} "
                f"The maze is too small to fit the {YELLOW}42{RESET} pattern."
            )
    print()
    print("A-Maze-ing")
    print("1. Generate fixed maze")
    print("2. Generate animated maze")
    print(f"3. Change algorithm. Current: {maze.algorithm}")
    print("4. Show/Hide the shortest path")
    print("5. Rotate the wall colours")
    print("6. Color gambling")
    print("7. Quit")
    print()
    print("Press a number (1-6) to select an option: ", end="", flush=True)


def fixed_maze(
    maze: MazeGenerator,
) -> tuple[list[list[int]], list[Wall]]:
    """Generate a fixed maze."""
    grid = maze.generate()
    solution = maze.get_solution()

    return grid, solution


def animated_maze(
    maze: MazeGenerator,
    renderer: TerminalRenderer,
) -> tuple[list[list[int]], list[Wall]]:
    """Generate and animate a maze."""
    solution: list[Wall] = []
    grid: list[list[int]] = []
    # Animación de la generación del maze
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

    # Animación de la solución
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
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py config.txt")
        return

    try:
        config = config_parsing.config_parser(sys.argv[1])
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

    # ---------------------------------------------------------
    # Entramos en la pantalla alternativa.
    # ---------------------------------------------------------
    start_screen()

    show_solution = True
    dfs = True
    renderer = TerminalRenderer()
    try:
        # Primer maze
        grid, solution = fixed_maze(maze)

        while running:

            # -------------------------------------------------
            # Dibujamos siempre la pantalla completa.
            # -------------------------------------------------
            draw_screen(
                maze,
                grid,
                solution,
                show_solution,
                renderer,
            )

            # -------------------------------------------------
            # Esperamos una tecla.
            # -------------------------------------------------
            option = get_key()

            # -------------------------------------------------
            # Procesamos la opción.
            # -------------------------------------------------
            match option:
                case "1":
                    maze.seed = random.randint(1, 100)
                    grid, solution = fixed_maze(maze)
                case "2":
                    maze.seed = random.randint(1, 100)
                    grid, solution = animated_maze(maze, renderer)
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
        # -----------------------------------------------------
        # Pase lo que pase, restauramos la terminal.
        # -----------------------------------------------------
        end_screen()


if __name__ == "__main__":
    main()
