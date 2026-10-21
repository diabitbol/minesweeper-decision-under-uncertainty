"""Local deductions followed by random frontier or board guesses."""
n = 8
mines_no = 8
import random
import os
import numpy as np
import numpy.random as rd
import numpy.linalg as alg
from . import linear_system
from . import deductions
import sys
import math

def print_mines_layout():
    global mine_values
    global n
    print()
    print('\t\t\tMINESWEEPER\n')
    st = '   '
    for i in range(n):
        st = st + '     ' + str(i + 1)
    print(st)
    for r in range(n):
        st = '     '
        if r == 0:
            for col in range(n):
                st = st + '______'
            print(st)
        st = '     '
        for col in range(n):
            st = st + '|     '
        print(st + '|')
        st = '  ' + str(r + 1) + '  '
        for col in range(n):
            st = st + '|  ' + str(mine_values[r][col]) + '  '
        print(st + '|')
        st = '     '
        for col in range(n):
            st = st + '|_____'
        print(st + '|')
    print()

def print_mines_layout2(mine_values):
    global n
    print()
    print('\t\t\tMINESWEEPER\n')
    st = '   '
    for i in range(n):
        st = st + '     ' + str(i + 1)
    print(st)
    for r in range(n):
        st = '     '
        if r == 0:
            for col in range(n):
                st = st + '______'
            print(st)
        st = '     '
        for col in range(n):
            st = st + '|     '
        print(st + '|')
        st = '  ' + str(r + 1) + '  '
        for col in range(n):
            st = st + '|  ' + str(mine_values[r][col]) + '  '
        print(st + '|')
        st = '     '
        for col in range(n):
            st = st + '|_____'
        print(st + '|')
    print()

def set_mines():
    """Place mines uniformly without replacement on the square board."""
    global numbers
    global mines_no
    global n
    count = 0
    while count < mines_no:
        val = random.randint(0, n * n - 1)
        r = val // n
        col = val % n
        if numbers[r][col] != -1:
            count = count + 1
            numbers[r][col] = -1

def set_values():
    """Count adjacent mines for every safe cell."""
    global numbers
    global n
    for r in range(n):
        for col in range(n):
            if numbers[r][col] == -1:
                continue
            if r > 0 and numbers[r - 1][col] == -1:
                numbers[r][col] = numbers[r][col] + 1
            if r < n - 1 and numbers[r + 1][col] == -1:
                numbers[r][col] = numbers[r][col] + 1
            if col > 0 and numbers[r][col - 1] == -1:
                numbers[r][col] = numbers[r][col] + 1
            if col < n - 1 and numbers[r][col + 1] == -1:
                numbers[r][col] = numbers[r][col] + 1
            if r > 0 and col > 0 and (numbers[r - 1][col - 1] == -1):
                numbers[r][col] = numbers[r][col] + 1
            if r > 0 and col < n - 1 and (numbers[r - 1][col + 1] == -1):
                numbers[r][col] = numbers[r][col] + 1
            if r < n - 1 and col > 0 and (numbers[r + 1][col - 1] == -1):
                numbers[r][col] = numbers[r][col] + 1
            if r < n - 1 and col < n - 1 and (numbers[r + 1][col + 1] == -1):
                numbers[r][col] = numbers[r][col] + 1

def neighbours(r, col):
    """Reveal the zero-connected region and its numbered neighbors."""
    global mine_values
    global numbers
    global visited
    if [r, col] not in visited:
        visited.append([r, col])
        if numbers[r][col] == 0:
            mine_values[r][col] = numbers[r][col]
            if r > 0:
                neighbours(r - 1, col)
            if r < n - 1:
                neighbours(r + 1, col)
            if col > 0:
                neighbours(r, col - 1)
            if col < n - 1:
                neighbours(r, col + 1)
            if r > 0 and col > 0:
                neighbours(r - 1, col - 1)
            if r > 0 and col < n - 1:
                neighbours(r - 1, col + 1)
            if r < n - 1 and col > 0:
                neighbours(r + 1, col - 1)
            if r < n - 1 and col < n - 1:
                neighbours(r + 1, col + 1)
        if numbers[r][col] != 0:
            mine_values[r][col] = numbers[r][col]

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def instructions():
    print('Instructions:')
    print('1. Enter row and column number to select a cell, Example "2 3"')
    print('2. In order to flag a mine, enter F after row and column numbers, Example "2 3 F"')

def check_over():
    global mine_values
    global n
    global mines_no
    count = 0
    for r in range(n):
        for col in range(n):
            if mine_values[r][col] != ' ' and mine_values[r][col] != 'F':
                count = count + 1
    if count == n * n - mines_no:
        return True
    else:
        return False

def show_mines():
    global mine_values
    global numbers
    global n
    for r in range(n):
        for col in range(n):
            if numbers[r][col] == -1:
                mine_values[r][col] = 'M'

def play_game(strategy):
    """Play one game using module-level board state. The first click may hit a mine."""
    global visited
    global n
    global mines_no
    global numbers
    numbers = [[0 for y in range(n)] for x in range(n)]
    global mine_values
    mine_values = [[' ' for y in range(n)] for x in range(n)]
    flags = []
    guess_count = 0
    set_mines()
    set_values()
    over = False
    while not over:
        if len(frontier(mine_values)) > 0:
            constraints = build_constraints(mine_values)
            solve = deductions.solve(constraints)
            if deductions.has_known_cell(solve):
                decision = deductions.first_known_cell(solve)
                front = frontier(mine_values)
                cell = front[decision[0]]
                if decision[1] == 'Safe':
                    inp = str(cell[0]) + ' ' + str(cell[1])
                else:
                    inp = str(cell[0]) + ' ' + str(cell[1]) + 'F'
            else:
                guess_count += 1
                if strategy == 'frontier':
                    inp = random_frontier_move(mine_values)
                elif strategy == 'board':
                    inp = random_board_move(mine_values)
        else:
            guess_count += 1
            inp = random_board_move(mine_values)
        if inp[-1] == 'F' or inp[-1] == 'f':
            inp2 = inp[:-1]
            val2 = inp2.split()
            val = []
            for i in range(len(val2)):
                val.append(int(val2[i]))
            r = val[0]
            col = val[1]
            if [r, col] in flags:
                print('Flag already set')
                continue
            if mine_values[r][col] != ' ':
                print('Value already known')
                continue
            if len(flags) < mines_no:
                flags.append([r, col])
                mine_values[r][col] = 'F'
            else:
                print('Flags finished')
                continue
        else:
            val2 = inp.split()
            val = []
            for i in range(len(val2)):
                val.append(int(val2[i]))
            r = val[0]
            col = val[1]
            if [r, col] in flags:
                flags.remove([r, col])
            if numbers[r][col] == -1:
                mine_values[r][col] = 'M'
                show_mines()
                over = True
                return (0.0, 0)
                continue
            elif numbers[r][col] == 0:
                visited = []
                mine_values[r][col] = '0'
                neighbours(r, col)
            else:
                mine_values[r][col] = numbers[r][col]
        if check_over():
            show_mines()
            over = True
            return (1.0, guess_count)
            continue

def info(board, i, j, known_mines):
    neighbors = neighborhood(i, j)
    known_mines = board[i][j]
    unvisited = []
    for ele in neighbors:
        if board[ele[0]][ele[1]] == 'F':
            known_mines -= 1
            known_mines.append((ele[0], ele[1]))
        elif board[ele[0]][ele[1]] == ' ':
            unvisited.append((ele[0], ele[1]))
    return (i, j, unvisited, known_mines, known_mines)

def frontier(board):
    """Return hidden cells adjacent to revealed numbered cells."""
    res = []
    for i in range(len(board)):
        for j in range(len(board[0])):
            frontier = False
            if board[i][j] == ' ':
                neighbors = neighborhood(i, j)
                for ele in neighbors:
                    if board[ele[0]][ele[1]] in [1, 2, 3, 4, 5, 6, 7, 8]:
                        frontier = True
            if frontier:
                res.append((i, j))
    return res

def neighborhood(r, col):
    global n
    neighbors = []
    if r > 0:
        neighbors.append((r - 1, col))
    if r < n - 1:
        neighbors.append((r + 1, col))
    if col > 0:
        neighbors.append((r, col - 1))
    if col < n - 1:
        neighbors.append((r, col + 1))
    if r > 0 and col > 0:
        neighbors.append((r - 1, col - 1))
    if r > 0 and col < n - 1:
        neighbors.append((r - 1, col + 1))
    if r < n - 1 and col > 0:
        neighbors.append((r + 1, col - 1))
    if r < n - 1 and col < n - 1:
        neighbors.append((r + 1, col + 1))
    return neighbors

def is_boundary(board, i, j):
    is_boundary = False
    if board[i][j] in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
        neighbors = neighborhood(i, j)
        for ele in neighbors:
            if board[ele[0]][ele[1]] == ' ':
                is_boundary = True
    return is_boundary

def boundary_cells(board):
    """Return revealed numbered cells adjacent to hidden cells."""
    res = []
    for i in range(len(board)):
        for j in range(len(board)):
            if is_boundary(board, i, j):
                res.append((i, j))
    return res

def random_frontier_move(board):
    front = frontier(board)
    p = len(front)
    k = random.randint(0, p - 1)
    a = front[k]
    return str(a[0]) + ' ' + str(a[1])

def random_board_move(board):
    a = 0
    while a != ' ':
        i = random.randint(0, n - 1)
        j = random.randint(0, n - 1)
        a = board[i][j]
    return str(i) + ' ' + str(j)

def build_constraints(board):
    """Express each boundary clue as frontier indices and a mine count."""
    bord = boundary_cells(board)
    front = frontier(board)
    res = []
    for ele in bord:
        neighbors = neighborhood(ele[0], ele[1])
        mine_count = board[ele[0]][ele[1]]
        a = []
        for i in neighbors:
            if board[i[0]][i[1]] == ' ':
                a.append(front.index(i))
            elif board[i[0]][i[1]] == 'F':
                mine_count -= 1
        res.append((a, mine_count))
    return res

def evaluate(trials, m, k, mode):
    """Run repeated games with the project strategy and counting convention."""
    global n
    global mines_no
    n = m
    mines_no = k
    wins = 0
    guess_count = 0
    vic = 0
    for l in range(trials):
        a, b = play_game(mode)
        wins += a
        vic += 1
        guess_count += b
    return (wins / trials, guess_count / vic)

def report(trials, m, k, mode):
    a, b = evaluate(trials, m, k, mode)
    print('Random strategy:', mode, 'size =', m, ' mines =', k, ' win rate =', a, trials, 'trials; project guess statistic =', b, ' guesses')

def evaluate_grid(mode):
    global n
    global mine_values
    N = [i for i in range(0, 14)]
    MINES_NO = [i for i in range(0, 14)]
    plot_results = [[0 for i in range(0, 14)] for j in range(0, 14)]
    for i in range(len(plot_results)):
        for j in range(len(plot_results[0])):
            if i >= 1 and j >= 1:
                if MINES_NO[j] < N[i] ** 2:
                    plot_results[j][i] = evaluate(1000, N[i], MINES_NO[j], mode)[0]
                    print(N[i], MINES_NO[j], plot_results[j][i])
    return plot_results

def plot_board_results(plot_results):
    import matplotlib.pyplot as plt
    global n
    global mines_values
    f = np.array(plot_results)
    plt.imshow(f, interpolation='nearest', origin='upper')
    plt.axis([1.5, 13.5, 1.5, 13.5])
    plt.xlabel('Board side length')
    plt.ylabel('Number of mines')
    plt.title('Random board strategy')
    plt.colorbar()
    plt.show()

def plot_frontier_results(plot_results):
    import matplotlib.pyplot as plt
    global n
    global mines_values
    f = np.array(plot_results)
    plt.imshow(f, interpolation='nearest', origin='upper')
    plt.axis([1.5, 13.5, 1.5, 13.5])
    plt.xlabel('Board side length')
    plt.ylabel('Number of mines')
    plt.title('Random frontier strategy')
    plt.colorbar()
    plt.show()
