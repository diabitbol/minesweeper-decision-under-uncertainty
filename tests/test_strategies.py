"""Small mathematical checks for the preserved research algorithms."""

import contextlib
import importlib
import io
import unittest

import numpy as np

from minesweeper import deductions, informed_strategy, linear_system, openings


class StrategyTests(unittest.TestCase):
    def test_deductions_propagate_across_constraints(self):
        self.assertEqual(
            deductions.solve([([0, 1], 1), ([0], 1), ([1, 2], 0)]),
            ['Mine', 'Safe', 'Safe'],
        )

    def test_ambiguous_clue_stays_unknown(self):
        self.assertEqual(deductions.solve([([0, 1], 1)]), ['Unknown', 'Unknown'])

    def test_sampler_respects_simple_binary_equation(self):
        np.random.seed(7)
        matrix = np.array([[1., 1.]])
        rhs = np.array([1.])
        candidates = linear_system.solutions(matrix, rhs, samples=100)
        self.assertEqual(len(candidates), 100)
        self.assertEqual({tuple(x) for x in candidates}, {(0, 1), (1, 0)})
        for x in candidates:
            np.testing.assert_allclose(matrix @ x, rhs)

    def test_frontier_and_system_subtract_flagged_mines(self):
        informed_strategy.n = 2
        board = [[1, 'F'], [' ', ' ']]
        self.assertEqual(set(informed_strategy.frontier(board)), {(1, 0), (1, 1)})
        matrix, rhs = informed_strategy.build_system(board)
        np.testing.assert_array_equal(matrix, [[1., 1.]])
        np.testing.assert_array_equal(rhs, [0.])

    def test_zero_mine_opening_reveals_entire_board(self):
        previous = openings.n, openings.mines_no
        try:
            openings.n, openings.mines_no = 3, 0
            self.assertEqual(openings.opening_size(0, 0), 9)
        finally:
            openings.n, openings.mines_no = previous

    def test_imports_do_not_start_experiments(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            for name in ['deduction_strategy', 'random_strategy', 'informed_strategy', 'opening_plots']:
                importlib.reload(importlib.import_module('minesweeper.' + name))
        self.assertEqual(output.getvalue(), '')


if __name__ == '__main__':
    unittest.main()
