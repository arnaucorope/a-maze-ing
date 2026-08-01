from mazegen import MazeGenerator


def test_algorithm(algorithm_name: str, perfect: bool) -> None:
    print(
        f"\nTesting algorithm={algorithm_name}, "
        f"perfect={perfect}"
    )

    generator = MazeGenerator(
        width=20,
        height=20,
        entry=(0, 0),
        exit_=(19, 19),
        perfect=perfect,
        seed=42,
        algorithm=algorithm_name,
    )

    grid = generator.generate()
    solution = generator.get_solution()

    print("Grid rows:", len(grid))
    print("Grid columns:", len(grid[0]))
    print("Solution length:", len(solution))
    print("Generation completed correctly")


def test_same_seed(algorithm_name: str) -> None:
    print(f"\nTesting same seed with {algorithm_name}")

    first_generator = MazeGenerator(
        width=20,
        height=20,
        entry=(0, 0),
        exit_=(19, 19),
        perfect=True,
        seed=42,
        algorithm=algorithm_name,
    )

    second_generator = MazeGenerator(
        width=20,
        height=20,
        entry=(0, 0),
        exit_=(19, 19),
        perfect=True,
        seed=42,
        algorithm=algorithm_name,
    )

    first_grid = first_generator.generate()
    second_grid = second_generator.generate()

    if first_grid != second_grid:
        raise AssertionError(
            f"{algorithm_name}: same seed generated different mazes"
        )

    print("Same seed generated the same maze")


def main() -> None:
    test_algorithm("dfs", True)
    test_algorithm("dfs", False)

    test_algorithm("prim", True)
    test_algorithm("prim", False)

    test_same_seed("dfs")
    test_same_seed("prim")

    print("\nAll generator tests passed")


if __name__ == "__main__":
    main()


