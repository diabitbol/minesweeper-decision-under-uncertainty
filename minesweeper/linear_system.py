"""Historical NumPy sampler for binary linear-system solutions."""
import numpy as np
import numpy.random as rd
import numpy.linalg as alg

def random_test_matrix(p=0.3):
    testA = np.zeros((5, 10))
    testA[0, 0:3] = [1, 0, 1]
    testA[4, 0:3] = [1, 0, 1]
    testA[1:4, :] = rd.rand(3, 10) < p
    return testA

def independent_subsystem(A):
    """Select independent rows and columns forming a maximum-rank square matrix."""
    n, p = A.shape
    r = alg.matrix_rank(A)
    B = np.zeros((r, p))
    row_index = 0
    current_rank = 0
    i = 0
    selected_rows = []
    while current_rank < r:
        B[row_index, :] = A[i, :]
        rp = alg.matrix_rank(B)
        if rp > current_rank:
            current_rank = rp
            row_index += 1
            selected_rows.append(i)
        i += 1
    C = np.zeros((r, r))
    column_index = 0
    current_rank = 0
    j = 0
    selected_columns = []
    while current_rank < r:
        C[:, column_index] = B[:, j]
        rp = alg.matrix_rank(C)
        if rp > current_rank:
            current_rank = rp
            column_index += 1
            selected_columns.append(j)
        j += 1
    return (C, selected_rows, selected_columns)

def solutions(A, B, exhaustive=False, samples=1000):
    """Sample binary assignments of free variables and solve for pivot variables.

Duplicates are retained, as in the historical implementation. Exhaustive
enumeration is not implemented. See docs/implementation-notes.md."""
    n, p = A.shape
    C, cl, cc = independent_subsystem(A)
    BB = B[cl]
    free_columns = [k for k in range(p) if k not in cc]
    Caux = A[cl, :]
    Caux = Caux[:, free_columns]
    Cinv = alg.inv(C)
    if exhaustive:
        return 'Exhaustive enumeration is not implemented.'
    else:
        proposals = []
        for _ in range(samples):
            X = rd.randint(0, 2, p)
            Xaux = X[free_columns]
            rhs = BB - Caux.dot(Xaux)
            Y = Cinv.dot(rhs)
            YY = Y * (1 - Y)
            if max(abs(YY)) < 1e-06:
                X[cc] = Y
                proposals.append(X)
        return proposals
