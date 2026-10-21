# Scientific report

## Research question

How can an algorithm improve its chance of winning Minesweeper when the visible
clues no longer yield an immediate safe move? This project studies first-click
openings, local deductions, binary linear systems, and probability-based move
selection. Improving the probability of winning is the main objective;
information-gain optimization remains a possible extension.

## Board model and vocabulary

Mines are placed uniformly on a square board with a fixed total mine count.
A safe cell displays the number of mines in its neighborhood: horizontally,
vertically, and diagonally adjacent cells within the board.

An **opening**, in Minesweeper terminology, is the region automatically revealed
by clicking a zero-clue cell. The reveal spreads through connected zero-clue
cells and includes their numbered boundary. In the first-click measurements,
opening size is zero for a mine hit, one for a safe numbered cell, and the full
revealed cell count when an opening is triggered.

- **Boundary:** revealed numbered cells with adjacent hidden, unflagged cells.
- **Frontier:** hidden, unflagged cells adjacent to revealed numbered cells.
- **Outside region:** hidden, unflagged cells not in the frontier.

| Revealed boundary | Hidden frontier |
| --- | --- |
| ![Boundary cells in green](figures/boundary.png) | ![Frontier cells in orange](figures/frontier.png) |

These diagrams show the same board. Green outlines the revealed clues that
constrain hidden neighbors; orange outlines the hidden cells those clues concern.
In the Python board, a blank string means hidden, `F` means flagged, and integers
represent revealed clues. A separate ground-truth board represents mines by
`-1`. The mathematical model assumes flagged cells are actual mines.

## First-click experiments

For each starting cell, repeated random 8 × 8 boards with eight mines estimate
the probability of triggering an opening and the mean number of revealed cells.

![Probability of triggering an opening](figures/opening-probability.png)

**Opening probability** is the proportion of trials revealing more than one cell.
Its color scale is a probability, rather than a cell count.

![Mean opening size](figures/mean-opening-size.png)

**Mean opening size** counts revealed cells, including zero for a mine hit.
The experiment shows larger mean openings near the perimeter, especially at
corners. This alone does not prove that a corner maximizes the eventual win rate.

![Reveal frequency for an upper-left first click](figures/corner-reveal-frequency.png)

**Spatial extent of a corner opening:** each cell's color shows how often it was
revealed after an upper-left first click. These heatmaps use zero-based row and
column coordinates, so that corner is (0, 0).

The strategy-comparison code starts with a random hidden cell rather than always
choosing a corner. First-click opening size and whole-game success are therefore
related but distinct experimental questions.

## Certain local deductions

For one revealed clue, define $v$ as its displayed mine count, $f$ as the number
of adjacent flagged cells, and $u$ as the number of adjacent hidden, unflagged
cells. The remaining adjacent mine count is $v-f$.

- If $v-f=0$, all $u$ unknown neighbors are safe.
- If $v-f=u$, all $u$ unknown neighbors are mines.

For example, a clue of 1 next to one flagged mine allows all its other unknown
neighbors to be revealed safely. A clue of 2 with exactly two unknown neighbors
and no flags identifies both as mines.

The solver repeats these rules until no status changes. Failure to advance under
these local rules does not prove that no certain move follows from all constraints.

## Notation for the linear model

Fix a visible board state. The following symbols describe that state and are
updated when cells are revealed or flagged.

| Symbol | Definition |
| --- | --- |
| $\mathcal B$ | Set of revealed boundary cells. |
| $\mathcal F$ | Set of hidden, unflagged frontier cells. |
| $L=\lvert\mathcal B\rvert$ | Number of boundary cells; bars denote the number of elements in a set. |
| $K=\lvert\mathcal F\rvert$ | Number of frontier cells. |
| $d_i$, $i=1,\ldots,L$ | Boundary cell numbered $i$. |
| $c_k$, $k=1,\ldots,K$ | Frontier cell numbered $k$. |
| $N(d_i)$ | Set of neighbors of $d_i$, including diagonals. |
| $v_i$ | Clue displayed at $d_i$. |
| $f_i$ | Number of flagged neighbors of $d_i$. |
| $x_k\in\{0,1\}$ | Mine indicator for $c_k$: 1 for a mine, 0 for a safe cell. |
| $x=(x_1,\ldots,x_K)^T$ | Column vector of frontier indicators; $T$ denotes transpose. |
| $A_{ik}$ | Matrix entry equal to 1 if $c_k$ neighbors $d_i$, and 0 otherwise. |
| $b_i=v_i-f_i$ | Number of mines still to locate around $d_i$. |
| $b=(b_1,\ldots,b_L)^T$ | Column vector of remaining clue counts. |

Each boundary cell imposes one equation:

$$\sum_{\substack{1\leq k\leq K\\c_k\in N(d_i)}}x_k=v_i-f_i,
\qquad i=1,\ldots,L.$$

The sum runs over frontier cells neighboring boundary cell $d_i$. Combining all
equations gives the binary linear system

$$Ax=b,\qquad x\in\{0,1\}^K.$$

The matrix $A$ has $L$ rows and $K$ columns. A binary solution is a frontier mine
arrangement consistent with the clues. For instance, $x_1+x_2+x_3=1$ means that
exactly one of three frontier cells contains a mine.

Selecting independent rows and columns identifies **pivot variables**, computed
by solving an invertible subsystem, and **free variables**, whose values must be
assigned first. The code samples binary assignments for the free variables and
solves for the pivot values with NumPy.

Agreement in every globally compatible arrangement would establish a certain
cell status. Agreement across only a finite sample cannot establish certainty.

## Probability model

Frontier arrangements need not be equally likely: using more mines on the
frontier leaves fewer mines to place elsewhere. Introduce these additional symbols.

| Symbol | Definition |
| --- | --- |
| $M$ | Mines remaining after subtracting all flags from the board's total mine count. |
| $U$ | Number of hidden, unflagged cells outside the frontier. |
| $s=(s_1,\ldots,s_K)$ | Candidate binary frontier arrangement; $s_k$ is the mine indicator for $c_k$. |
| $m(s)=\sum_{k=1}^K s_k$ | Number of frontier mines in arrangement $s$. |
| $\mathcal S$ | Arrangements satisfying the clue equations and $0\leq M-m(s)\leq U$. |
| $\binom{U}{r}$ | Number of ways to choose $r$ mine positions among $U$ outside cells. |
| $w(s)$ | Number of full-board placements extending arrangement $s$. |
| $Z$ | Total number of compatible full-board mine placements. |
| $P(x_k=1\mid\text{visible clues})$ | Probability that $c_k$ is mined given the clues, flags, and fixed mine count. |

Arrangement $s$ leaves $M-m(s)$ mines outside the frontier, so its weight is

$$w(s)=\binom{U}{M-m(s)}.$$

Summing over all arrangements in $\mathcal S$ gives

$$Z=\sum_{s\in\mathcal S}w(s).$$

For a consistent board state, $Z>0$. The mine probability for cell $c_k$ is

$$P(x_k=1\mid\text{visible clues})=
\frac{\sum_{s\in\mathcal S}s_k\,w(s)}{Z}.$$

The numerator counts compatible full-board placements with a mine at $c_k$;
the denominator counts all compatible placements. This explains why an unweighted
average of frontier arrangements need not give the correct probability.

### Implemented approximation

The code averages sampled indicators rather than applying these weights. Define
$H$ as the number of accepted samples, $s^{(h)}$ as accepted sample number $h$,
and $s_k^{(h)}$ as its indicator for cell $c_k$. For $H>0$, it computes

$$\widehat p_k=\frac{1}{H}\sum_{h=1}^H s_k^{(h)}.$$

Here $\widehat p_k$ is the estimated mine frequency at $c_k$; repeated samples
are retained. It is not the exact weighted probability above. A sample frequency
of zero or one does not prove a cell's status. If no candidate is found, the
strategy falls back to a random hidden board cell. Numerical limitations are
described in the [implementation notes](implementation-notes.md).

## Strategy comparison

All three strategies exhaust local deductions before guessing. **Random frontier**
selects a hidden frontier cell, **random board** selects a hidden, unflagged cell
anywhere, and **informed** selects a frontier cell with a low sampled mine frequency.

![Win rates for the three strategies](figures/reported-win-rates.png)

The project experiments give win rates of 59%, 56%, and 47% for informed,
random-board, and random-frontier strategies on 8 × 8 boards with eight mines.
The informed strategy also performs better in the two larger configurations
studied; the full table is in the README. These observations motivate informed
selection but do not establish optimality.

Values are stored in [`reported-win-rates.csv`](../data/reported-win-rates.csv).
Regenerate the chart with `python scripts/plot_reported_results.py` from the root.

## Limitations and extensions

The available experiment records do not retain all random seeds, trial counts,
and code revisions. New runs therefore produce their own estimates.

The sampler treats frequencies of zero or one as certainty. Exact enumeration,
global mine-count weighting, independent frontier components, controlled benchmark
protocols, and an explicit information-gain objective are possible extensions.
Distinguishing the theoretical probability model from its implemented approximation
is essential to interpreting the results.
