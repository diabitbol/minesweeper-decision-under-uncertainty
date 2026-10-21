# Scientific summary

## Research question and scope

The project studies decision-making under uncertainty through Minesweeper:
how can an algorithm improve its chance of revealing all safe cells when the
visible clues do not determine a certain move?

The work combines first-click experiments, local deduction rules, linear algebra,
and probabilistic move selection. Maximizing the probability of winning is the
main practical objective. The notes also consider the information gained from a
move, but do not establish a completed information-gain optimization method.

## Board model

A square board contains a fixed number of uniformly placed mines. A revealed safe
cell displays the number of mines in its neighborhood, including diagonals.
Revealing a zero expands automatically through neighboring safe cells.

- **Boundary:** revealed numbered cells with at least one adjacent hidden cell.
- **Frontier:** hidden cells adjacent to revealed numbered cells.
- **Outside region:** hidden, unflagged cells outside the frontier.

| Revealed boundary | Hidden frontier |
| --- | --- |
| ![Revealed boundary cells outlined in green](figures/boundary.png) | ![Hidden frontier cells outlined in orange](figures/frontier.png) |

Original diagrams from slides 5 and 6. The green outline follows revealed
numbered cells that constrain hidden neighbors; the orange outline follows
adjacent hidden cells whose mine status is unknown. Both show the same board.

The historical Python representation uses a blank string for a hidden cell,
`F` for a flagged mine, and integers for revealed clues. Mines in the hidden
ground-truth board are represented by `-1`.

## First-click experiments

For each possible starting cell, repeated randomly generated boards estimate the
mean number of cells revealed and the probability of an opening larger than one
cell. A click on a mine contributes zero; a safe numbered cell contributes one.

The presentation and working notes report larger mean openings near the board's
edges, especially its corners, for the studied configuration. This concerns
opening size, rather than proving that a corner maximizes the eventual win rate.
The saved game strategies themselves begin with a random hidden cell.

### Saved first-click figures

![Mean opening size by starting position](figures/mean-opening-size.png)

**Mean opening size.** The color scale counts the cells revealed automatically
after the first click, with zero assigned to a mine hit. The saved output shows
larger mean openings near the perimeter, especially at corners.

![Probability of revealing more than one cell](figures/opening-probability.png)

**Opening probability.** This is a different quantity: the probability that the
first click reveals more than one cell. Its scale is a probability, not a number
of revealed cells. This distinction also resolves a mislabeled heading in the
original presentation; see [figure provenance](figures/README.md).

![Reveal frequency for an upper-left first click](figures/corner-reveal-frequency.png)

**Spatial extent of a corner opening.** Each cell's color shows its saved reveal
frequency for a first click at position (0, 0). Exact trial counts and seeds for
these saved images are not established by the surviving figure files.

## Certain local deductions

For a clue with value $v$, let $f$ be the number of adjacent flagged mines and $u$
the number of adjacent unknown cells.

- If $v-f=0$, every adjacent unknown cell is safe.
- If $v-f=u$, every adjacent unknown cell is a mine.

The solver repeats these rules until no status changes. This is a local
propagation method: failure to find a move does not prove that no logically
certain move exists under the complete set of constraints.

## Binary linear-system model

Number the frontier cells and assign a variable $x_k\in\{0,1\}$ to each, with
one indicating a mine. Each boundary clue supplies an equation:

$$\sum_{k\in N(c)\cap\mathcal F}x_k=v_c-f_c.$$

Together, the equations form $Ax=b$. Selecting independent rows and columns
identifies pivot and free variables. The saved implementation samples binary
values of the free variables and solves for the pivots using NumPy.

Over **all** compatible configurations, a variable fixed at zero or one would
provide a certain deduction. Agreement across only a finite sample cannot
establish that certainty.

## Exact probability model discussed in the notes

Frontier assignments are generally not equally likely once the total mine count
is taken into account. Let $M$ be the number of unflagged mines remaining, $U$ the
number of hidden cells outside the frontier, and $m(s)$ the number of mines in a
compatible frontier assignment $s$. Under a uniform fixed-mine-count board model,
that assignment has weight

$$w(s)=\binom{U}{M-m(s)},$$

with zero weight when the remaining mine count cannot fit outside the frontier.
Thus, for a frontier cell $k$,

$$P(x_k=1\mid\text{visible clues})=
\frac{\sum_s x_k(s)w(s)}{\sum_s w(s)}.$$

The notes illustrate this with frontier assignments containing different numbers
of mines, which leave different numbers of possible placements in the outside
region. This is the conceptual reason a simple average over frontier assignments
need not give the correct posterior probability.

The Python implementation instead averages the binary values returned by its
sampler. The exact weighted model above is documented research, not an implemented
feature of the published historical solver.

## Strategy comparison

All three guessing strategies first apply the local deduction rules. If those
rules cannot advance, the algorithm either selects a random hidden frontier cell,
selects a random hidden cell anywhere, or uses sampled frontier mine frequencies.
The informed strategy falls back to a random hidden board cell when its sampler
finds no candidate.

The final presentation reports win rates of 59%, 56%, and 47% respectively for
informed, random-board, and random-frontier strategies on 8 × 8 boards with eight
mines. The gap increases in its larger-board examples; the full table is in the
README. These historical observations support the motivation for informed
guesses, but are not a new benchmark or proof of optimality.

![Reported win rates for the three strategies](figures/reported-win-rates.png)

The chart redraws the final presentation's numerical table in English; it does
not rerun the experiments. Its source values are available in
[`reported-win-rates.csv`](../data/reported-win-rates.csv), and the rendering can
be reproduced with `python scripts/plot_reported_results.py` from the repository
root.

## Limits and possible extensions

The saved experiments have limited reproducibility metadata, and the approximate
sampler can mistake a sample frequency of zero or one for certainty. Exact binary
enumeration, global mine-count weighting, independent frontier components,
controlled benchmark protocols, and explicit information-gain objectives would
be natural extensions. They have intentionally not been introduced into this
moderate refactoring of the original project.
