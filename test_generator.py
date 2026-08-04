from app.renderer import TerminalRenderer
from mazegen.maze_generator import MazeGenerator


maze = MazeGenerator(
    width=15,
    height=15,
    entry=(0, 0),
    exit_=(14, 14),
    perfect=False,
    seed=4,
    algorithm="prim"
)

grid = maze.generate()

renderer = TerminalRenderer()
renderer.draw(grid, maze.entry, maze.exit_)
