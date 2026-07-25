from mazegen import MazeGenerator


generator = MazeGenerator(
    width=4,
    height=3,
    entry=(0, 0),
    exit_=(3, 2),
    perfect=True,
)
generator._grid[0][0] = 99
print(generator.width)
print(generator.height)
print(generator._grid)
