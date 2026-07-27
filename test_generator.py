from mazegen import MazeGenerator, Wall


generator = MazeGenerator(
    width=9,
    height=7,
    entry=(0, 0),
    exit_=(2, 2),
    perfect=True,
)

generator.generate()

for y, row in enumerate(generator._grid):
    line = ""

    for x, cell in enumerate(row):
        if (x, y) in generator._pattern_cells:
            line += "# "
        else:
            line += ". "

    print(line)
