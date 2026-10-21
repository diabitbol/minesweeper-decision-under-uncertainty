# Implementation notes

## Refactoring scope

This edition preserves the project algorithmic structure and module-level
board state. It translates identifiers, messages, and documentation into English,
removes obsolete commented-out drafts, and replaces automatic import-time
experiments with an explicit runner. It also makes console clearing work on
Windows. It is not a redesign of the game engine or a new exact solver.

| Original file | Published module |
| --- | --- |
| `jeu/solvers.py` | `minesweeper/deductions.py` |
| `jeu/systlin.py` | `minesweeper/linear_system.py` |
| `jeu/certitude.py` | `minesweeper/deduction_strategy.py` |
| `jeu/aleatoire.py` | `minesweeper/random_strategy.py` |
| `jeu/partie_auto.py` | `minesweeper/informed_strategy.py` |
| `jeu/simulation.py` | `minesweeper/openings.py` |
| `jeu/data.py` | `minesweeper/opening_plots.py` |

Other versions of the manual game, scratch scripts, duplicated text exports,
French drafts, caches, and downloaded research papers are omitted.

## Sampling limitations

The linear sampler selects independent rows and columns, assigns binary values
to free variables, and calculates pivot values by a matrix inverse. It accepts
values within a floating-point tolerance of zero or one and retains duplicates.
The default is 1,000 attempts; exhaustive enumeration remains unimplemented.

Several limitations of the original code are deliberately documented rather
than silently changing the project algorithm:

- It does not weight frontier assignments by outside mine placements or enforce
  the remaining global mine count.
- Its sampled frequencies are approximate. The strategy treats frequencies of
  zero or one as certain even though an unobserved compatible assignment may
  contradict them.
- After solving the selected independent equations, the sampler does not
  explicitly recheck every original equation. Inconsistent input constraints
  require particular care.
- Pivot values are assigned to an integer NumPy array after a floating-point
  calculation. Values slightly below one can be truncated; the project
  implementation does not round first.
- Rank-zero systems and unusual degenerate inputs are not handled as a general
  mathematical API. The module is retained for the original experiments.

Consequently, success rates measure this implementation, not an exact Bayesian
solver. Increasing the sample count alone does not fix these limitations.

## Experiment conventions

Mines are placed before the initial move; there is no first-click protection.
The initial move is uniformly random among hidden board cells. Square boards are
used throughout. A seed initializes both Python's and NumPy's random generators;
results can still depend on library versions and numerical linear algebra.

The deduction-only strategy stops when local deductions run out after a frontier
has formed. It can take another random move if no frontier exists, as in the
original code. This is not an exhaustive logical-solvability test.

The random strategy returns a guess count of zero for losing games. Its evaluator
divides the accumulated winning-game counts by **all trials**. The runner labels
this `winning_game_guess_total_per_trial`: it is neither the mean over all games
nor the mean conditioned on victory. A mean guess count conditioned on victory cannot be reconstructed from this
field alone without also retaining the win count.

The first-click plotting functions retain the original configuration convention:
their `n` argument controls the plot loops, while the actual board size and mine
count live in `minesweeper.openings.n` and `minesweeper.openings.mines_no`. When
changing sizes, set both explicitly. Plotting functions display interactive
Matplotlib figures and do not write files automatically.

## Verification

Run the focused checks from the repository root:

```bash
python -m unittest discover -s tests -v
```

The checks cover local deductions, a simple sampled system, frontier construction,
and import behavior. During preparation, seeded original/refactored comparisons
are also used to check preservation of the selected algorithms. Passing these
checks does not validate the experiment results or eliminate the documented
scientific limitations.
