"""Monte Carlo primitives for the first-click opening experiments."""
n = 8
mines_no = 8
import random
import os

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
    global revealed_count
    if [r, col] not in visited:
        visited.append([r, col])
        revealed_count += 1
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

def show_mines():
    global mine_values
    global numbers
    global n
    for r in range(n):
        for col in range(n):
            if numbers[r][col] == -1:
                mine_values[r][col] = 'M'

def opening_size(i, j):
    """Return the number of cells revealed by one click; a mine returns zero."""
    global visited
    global revealed_count
    global n
    global mines_no
    global numbers
    numbers = [[0 for y in range(n)] for x in range(n)]
    global mine_values
    mine_values = [[' ' for y in range(n)] for x in range(n)]
    flags = []
    set_mines()
    set_values()
    if numbers[i][j] == -1:
        return 0
    elif numbers[i][j] == 0:
        visited = []
        revealed_count = 1
        neighbours(i, j)
        return revealed_count - 1
    else:
        return 1

def reveal_neighbors_recorded(r, col):
    global mine_values
    global numbers
    global visited
    global revealed_count
    if [r, col] not in visited:
        visited.append([r, col])
        revealed_count += 1
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

def opening_cells(i, j):
    """Return opening size and visited cells using the historical traversal."""
    global visited
    global revealed_count
    global n
    global mines_no
    global numbers
    numbers = [[0 for y in range(n)] for x in range(n)]
    global mine_values
    mine_values = [[' ' for y in range(n)] for x in range(n)]
    flags = []
    set_mines()
    set_values()
    if numbers[i][j] == -1:
        return (0, 0)
    elif numbers[i][j] == 0:
        visited = []
        res = []
        revealed_count = 1
        reveal_neighbors_recorded(i, j)
        return (revealed_count - 1, visited)
    else:
        return (1, 0)
