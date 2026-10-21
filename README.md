# Decision under uncertainty: Minesweeper

**How should a Minesweeper player choose a move when logical deductions run out?**

This project explores that question through local deductions, binary linear systems,
and Monte Carlo experiments.

## The investigation

1. **First click:** measure the opening produced by each starting position.
2. **Certain moves:** propagate local constraints to identify safe cells and mines.
3. **Uninformed guesses:** compare random hidden cells on the frontier with random
   hidden cells across the board.
4. **Informed guesses:** model frontier cells as binary variables, sample compatible
   assignments, and choose a cell with a low estimated mine frequency.

The written research also discusses an exact probability model that weights
frontier configurations by the number of compatible placements outside the frontier.
The historical Python sampler does **not** implement that weighting or exhaustive
enumeration. Its estimates should not be interpreted as exact probabilities.

## Results reported at the oral presentation

| Square board | Mines | Informed strategy | Random board | Random frontier |
| --- | ---: | ---: | ---: | ---: |
| 8 × 8 | 8 | 59% | 56% | 47% |
| 16 × 16 | 40 | 41% | 29% | 23% |
| 22 × 22 | 99 | 11% | 1.4% | 0.6% |

These are **historical reported results**, transcribed from the final presentation.
The surviving files do not establish a complete reproducible record of their seeds,
trial counts, or exact code revision. Fresh runs will produce their own results.
The board sizes and mine counts above are the project's configurations; its
22 × 22 board is square.

## Run an experiment

Use Python 3.10 or later. From the repository root:

```bash
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# macOS / Linux:
# source .venv/bin/activate
python -m pip install -r requirements.txt

python simulate.py --strategy board --size 8 --mines 8 --trials 1000 --seed 42
python simulate.py --strategy frontier --trials 1000 --seed 42
python simulate.py --strategy deduction --trials 1000 --seed 42
python simulate.py --strategy informed --trials 100 --seed 42 --output results/informed.json
```

The `deduction` baseline permits the initial random move and stops when the local
rules cannot advance. The `informed` strategy uses 1,000 sampling attempts per
system by default and can be slow on larger boards. **The first click can hit a
mine** in these experiments.

For first-click heatmaps:

```python
from minesweeper import opening_plots

opening_plots.plot_mean_opening(8, 1000)
opening_plots.plot_opening_probability(8, 1000)
opening_plots.plot_reveal_probability(8, 1000, 0, 0)
```

These plotting functions use the default 8 × 8 / 8-mine configuration in
`minesweeper.openings`. See the implementation notes before changing board sizes.

## Repository guide

```text
minesweeper/
    deductions.py          Local constraint propagation
    deduction_strategy.py  Deduction-only baseline
    random_strategy.py     Random frontier and random board strategies
    linear_system.py       Binary solution sampler
    informed_strategy.py   Strategy using the sampler
    openings.py            First-click simulation primitives
    opening_plots.py       First-click heatmaps
docs/
    scientific-summary.md  Research question, model, and interpretation
    implementation-notes.md  Limitations and refactoring decisions
    references.md          Research sources and code provenance
simulate.py                Explicit experiment entry point
tests/                     Focused regression and mathematical checks
```

Read the [scientific summary](docs/scientific-summary.md) for the mathematical
model and the [implementation notes](docs/implementation-notes.md) for what the
surviving code does and does not establish.

## Provenance and reuse

The initial console game was based on the AskPython tutorial cited in the original
project notes. The research also draws on the sources listed in
[References](docs/references.md). The French working documents, original slides,
downloaded articles, and intermediate drafts are not included in this edition.

No license has been added to this repository. Third-party material retains its
own rights and terms; public availability does not grant a general reuse license.
