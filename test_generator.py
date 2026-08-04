import unittest

from mazegen import MazeGenerator


class TestMazeGenerator(unittest.TestCase):
    def _create_maze(
        self,
        algorithm: str = "dfs",
        perfect: bool = True,
        seed: int = 42,
    ) -> MazeGenerator:
        return MazeGenerator(
            width=20,
            height=20,
            entry=(0, 0),
            exit_=(19, 19),
            perfect=perfect,
            seed=seed,
            algorithm=algorithm,
        )

    def test_generate_returns_complete_grid(self) -> None:
        maze = self._create_maze()

        grid = maze.generate()

        self.assertEqual(len(grid), 20)

        for row in grid:
            self.assertEqual(len(row), 20)

        self.assertGreater(len(maze.get_solution()), 0)

    def test_generate_steps_produces_frames(self) -> None:
        maze = self._create_maze()
        step_count = 0

        for grid in maze.generate_steps():
            step_count += 1

            self.assertEqual(len(grid), 20)

            for row in grid:
                self.assertEqual(len(row), 20)

        self.assertGreater(step_count, 0)
        self.assertGreater(len(maze.get_solution()), 0)

    def test_generate_steps_with_dfs(self) -> None:
        maze = self._create_maze(
            algorithm="dfs",
            perfect=True,
        )
        step_count = 0

        for _ in maze.generate_steps():
            step_count += 1

        self.assertGreater(step_count, 0)
        self.assertGreater(len(maze.get_solution()), 0)

    def test_generate_steps_with_prim(self) -> None:
        maze = self._create_maze(
            algorithm="prim",
            perfect=True,
        )
        step_count = 0

        for _ in maze.generate_steps():
            step_count += 1

        self.assertGreater(step_count, 0)
        self.assertGreater(len(maze.get_solution()), 0)

    def test_generate_steps_imperfect_maze(self) -> None:
        maze = self._create_maze(
            algorithm="dfs",
            perfect=False,
        )
        step_count = 0

        for _ in maze.generate_steps():
            step_count += 1

        self.assertGreater(step_count, 0)
        self.assertGreater(len(maze.get_solution()), 0)

    def test_same_seed_produces_same_dfs_maze(self) -> None:
        first_maze = self._create_maze(
            algorithm="dfs",
            perfect=False,
            seed=42,
        )
        second_maze = self._create_maze(
            algorithm="dfs",
            perfect=False,
            seed=42,
        )

        first_grid = first_maze.generate()
        second_grid = second_maze.generate()

        self.assertEqual(first_grid, second_grid)
        self.assertEqual(
            first_maze.get_solution(),
            second_maze.get_solution(),
        )

    def test_same_seed_produces_same_prim_maze(self) -> None:
        first_maze = self._create_maze(
            algorithm="prim",
            perfect=False,
            seed=42,
        )
        second_maze = self._create_maze(
            algorithm="prim",
            perfect=False,
            seed=42,
        )

        first_grid = first_maze.generate()
        second_grid = second_maze.generate()

        self.assertEqual(first_grid, second_grid)
        self.assertEqual(
            first_maze.get_solution(),
            second_maze.get_solution(),
        )

    def test_solution_steps_matches_solution(self) -> None:
        maze = self._create_maze()
        maze.generate()

        directions: list = []

        for direction in maze.solution_steps():
            directions.append(direction)

        self.assertEqual(directions, maze.get_solution())

    def test_unknown_algorithm_raises_error(self) -> None:
        maze = self._create_maze()
        maze.algorithm = "unknown"

        with self.assertRaises(ValueError):
            maze.generate()


if __name__ == "__main__":
    unittest.main()



