"""Local constraint propagation for certain Minesweeper deductions."""
import numpy as np

def solve(I):
    """Propagate local safe-cell and all-mined deductions to a fixed point."""
    N = 0
    for x in I:
        N = max(N, max(x[0]))
    status = ['Unknown'] * (N + 1)
    ok = True
    while ok:
        ok = False
        for x in I:
            known_safe, known_mines, unknown_count = (0, 0, 0)
            for k in x[0]:
                unknown_count += status[k] == 'Unknown'
                known_mines += status[k] == 'Mine'
                known_safe += status[k] == 'Safe'
            if unknown_count > 0:
                if x[1] - known_mines == 0:
                    ok = True
                    for k in x[0]:
                        if status[k] == 'Unknown':
                            status[k] = 'Safe'
                if x[1] - known_mines == unknown_count:
                    ok = True
                    for k in x[0]:
                        if status[k] == 'Unknown':
                            status[k] = 'Mine'
    return status

def has_known_cell(res):
    for ele in res:
        if ele != 'Unknown':
            return True
    return False

def first_known_cell(res):
    """Return the first frontier index whose status is known."""
    for i in range(len(res)):
        if res[i] != 'Unknown':
            return (i, res[i])
