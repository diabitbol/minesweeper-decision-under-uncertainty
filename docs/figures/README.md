# Research figures

These figures illustrate the opening experiments, board model, and strategy
comparison. The numerical heatmaps are preserved research outputs; the comparison
chart is generated from the stored results table.

| File | Quantity or concept |
| --- | --- |
| `opening-probability.png` | Probability that a first click reveals more than one cell. |
| `mean-opening-size.png` | Mean number of cells revealed, including zero for a mine hit. |
| `corner-reveal-frequency.png` | Per-cell reveal frequency for an upper-left first click. |
| `boundary.png` | Revealed boundary cells outlined in green. |
| `frontier.png` | Hidden frontier cells outlined in orange. |
| `reported-win-rates.png` | Strategy win rates from `data/reported-win-rates.csv`. |

Opening probability has a probability scale; mean opening size counts revealed
cells. Rows run downwards and columns to the right. Heatmaps use zero-based
coordinates; board diagrams use one-based labels. Opening experiments use an
8 × 8 board with eight mines.

## Regenerate the comparison chart

After installing the requirements, run from the repository root:

```bash
python scripts/plot_reported_results.py
```

This reads stored research results rather than running simulations. Fresh opening
experiments use `minesweeper.opening_plots`. Raw matrices and exact simulation
parameters for the saved heatmaps are not included; new heatmaps need not match
these images exactly.
