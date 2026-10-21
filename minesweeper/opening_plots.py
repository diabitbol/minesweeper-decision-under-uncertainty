"""Project first-click heatmaps, with explicit plot entry points."""
n = 8
trials = 10000
from . import openings
import matplotlib.pyplot as plt
import numpy as np

def plot_mean_opening(n, trials):
    res = [[0 for j in range(n)] for i in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(trials):
                res[i][j] += openings.opening_size(i, j)
            res[i][j] /= trials
    f = np.array(res)
    plt.imshow(f, interpolation='nearest', origin='upper')
    plt.xlabel("Column")
    plt.ylabel("Row")
    plt.title('Mean first-click opening size')
    plt.colorbar()
    plt.show()

def plot_opening_probability(n, trials):
    res = [[0 for j in range(n)] for i in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(trials):
                res[i][j] += openings.opening_size(i, j) > 1
            res[i][j] /= trials
    f = np.array(res)
    plt.imshow(f, interpolation='nearest', origin='upper')
    plt.xlabel("Column")
    plt.ylabel("Row")
    plt.title('Probability of an opening larger than one cell')
    plt.colorbar()
    plt.show()

def plot_reveal_probability(n, trials, i, j):
    plot_results = [[0 for i in range(n)] for j in range(n)]
    for k in range(trials):
        simul = openings.opening_cells(i, j)
        if simul[0] > 1:
            for l in simul[1]:
                plot_results[l[0]][l[1]] += 1
        if simul[0] == 1:
            plot_results[i][j] += 1
    for i in range(len(plot_results)):
        for j in range(len(plot_results[0])):
            plot_results[i][j] /= trials
    f = np.array(plot_results)
    plt.imshow(f, interpolation='nearest', origin='upper')
    plt.xlabel("Column")
    plt.ylabel("Row")
    plt.title('Cell reveal frequency after the first click')
    plt.colorbar()
    plt.show()
