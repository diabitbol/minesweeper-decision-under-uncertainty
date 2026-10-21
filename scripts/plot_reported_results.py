"""Plot the project strategy-comparison results from the stored data."""

import csv
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


def main():
    root = Path(__file__).resolve().parents[1]
    with (root / 'data' / 'reported-win-rates.csv').open(encoding='utf-8', newline='') as stream:
        rows = list(csv.DictReader(stream))
    positions = np.arange(len(rows))
    fig, ax = plt.subplots(figsize=(10, 5.6), layout='constrained')
    series = [
        ('informed', 'Informed strategy', '#277b81'),
        ('random_board', 'Random board', '#5175aa'),
        ('random_frontier', 'Random frontier', '#d28b47'),
    ]
    for index, (key, label, color) in enumerate(series):
        values = [float(row[key]) * 100 for row in rows]
        bars = ax.bar(positions + (index - 1) * .25, values, width=.24, label=label, color=color)
        ax.bar_label(bars, labels=[f'{value:g}%' for value in values], padding=4, fontsize=10)
    ax.set_xticks(positions, [f"{r['size']} × {r['size']}\n{r['mines']} mines" for r in rows])
    ax.set_ylim(0, 72)
    ax.set_ylabel('Win rate (%)')
    ax.set_title('Minesweeper strategy comparison', pad=17)
    ax.legend(frameon=False, loc='upper right')
    ax.set_axisbelow(True)
    ax.grid(axis='y', alpha=.18)
    ax.spines[['top', 'right']].set_visible(False)
    output = root / 'docs' / 'figures' / 'reported-win-rates.png'
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output, dpi=180, bbox_inches='tight')
    plt.close(fig)
    print(output)


if __name__ == '__main__':
    main()
