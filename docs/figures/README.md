# Figure provenance

The original numerical heatmaps and board diagrams below were recovered from the
project's local files. Their pixels are preserved; they are not newly simulated
results. Captions supply English explanations because these numerical figures
do not contain prose labels. Raw numerical matrices, seeds, and exact trial counts
for the saved heatmaps are not available in this repository.

| File | Origin | Interpretation |
| --- | --- | --- |
| `mean-opening-size.png` | Original `modelisation1.png` | Mean number of cells revealed by a first click, including zero for a mine hit. |
| `opening-probability.png` | Original `modélisation2.png`; also embedded on slide 15 | Probability of revealing more than one cell. The original slide calls it a mean opening size, but the saved probability scale and written research identify this as the probability heatmap. |
| `corner-reveal-frequency.png` | Original `histogramme.png` | Saved per-cell reveal-frequency heatmap for a first click in the upper-left corner. |
| `boundary.png` | Image embedded on slide 5 of the final presentation | Revealed boundary cells outlined in green. |
| `frontier.png` | Image embedded on slide 6 of the final presentation | Hidden frontier cells outlined in orange. |
| `reported-win-rates.png` | New rendering of the values on slide 29 | Historical reported win rates; the values are stored in `data/reported-win-rates.csv`. |

Rows run downwards and columns run to the right. The opening heatmaps use
zero-based coordinates, while the presentation diagrams use one-based labels.
The first-click experiments use an 8 × 8 board with eight mines.

## Regenerate the comparison chart

From the repository root, after installing the requirements:

```bash
python scripts/plot_reported_results.py
```

The three original heatmaps are retained as saved historical outputs; this
command does not reconstruct them. Fresh opening experiments can be run through
`minesweeper.opening_plots`, but should not be substituted for historical images
without identifying them as new simulations.
