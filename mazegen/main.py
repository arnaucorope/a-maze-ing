from mazegen import MazeGenerator

def main():
    maze = MazeGenerator(10, 10, (0, 0), (9, 9), True, "42")
    maze.generate()

    with open("output_maze.txt", "w") as f:
        f.write("\n".join("".join(f"{cell:X}" for cell in row) for row in maze.grid) + "\n")

if __name__ == "__main__":
    main()

