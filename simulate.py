"""Run the historical experiments without starting work during imports."""

import argparse
import contextlib
import io
import json
import random
import sys
from pathlib import Path

import numpy as np


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--strategy', choices=['deduction', 'board', 'frontier', 'informed'], default='board')
    parser.add_argument('--size', type=int, default=8, help='Side length of the square board')
    parser.add_argument('--mines', type=int, default=8)
    parser.add_argument('--trials', type=int, default=100)
    parser.add_argument('--seed', type=int, default=42)
    parser.add_argument('--output', type=Path, help='Optional JSON result file')
    args = parser.parse_args()
    if args.size < 2 or not 1 <= args.mines < args.size ** 2 or args.trials < 1:
        parser.error('Require size >= 2, 1 <= mines < size squared, and trials >= 1.')
    from minesweeper import deduction_strategy, informed_strategy, random_strategy

    random.seed(args.seed)
    np.random.seed(args.seed)
    sys.setrecursionlimit(max(sys.getrecursionlimit(), args.size ** 2 * 2 + 100))
    module = {'deduction': deduction_strategy, 'informed': informed_strategy}.get(args.strategy, random_strategy)
    module.n, module.mines_no = args.size, args.mines
    # The legacy evaluator prints progress. Keep machine-readable output clean.
    with contextlib.redirect_stdout(io.StringIO()):
        if args.strategy in ['board', 'frontier']:
            win_rate, legacy_guess_statistic = module.evaluate(args.trials, args.size, args.mines, args.strategy)
        else:
            win_rate = module.evaluate(args.trials, args.size, args.mines)
            legacy_guess_statistic = None
    result = {
        'strategy': args.strategy, 'size': args.size, 'mines': args.mines,
        'trials': args.trials, 'seed': args.seed, 'win_rate': win_rate,
        'first_click_safe': False,
    }
    if legacy_guess_statistic is not None:
        result['winning_game_guess_total_per_trial'] = legacy_guess_statistic
    rendered = json.dumps(result, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered + '\n', encoding='utf-8')
    print(rendered)


if __name__ == '__main__':
    main()
