
from mazegen import MazeGenerator


generator = MazeGenerator(
    width=9,
    height=7,
    entry=(0, 0),
    exit_=(2, 2),
    perfect=True,
    seed=42,
    algorithm="dfs",
)

grid = generator.generate()

print(grid)
print(generator.get_solution())
