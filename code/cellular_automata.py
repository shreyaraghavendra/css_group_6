import numpy as np
import math
import random

# Constants
ROWS = 101
COLS = 101
ORIGIN = (COLS // 2, ROWS // 2)
K1, K2, K3, K4 = (0.7, 0.2, 0.3, 0.3)
PHI = ROWS * COLS
RHO = 3.85
GENERATIONS = 100
CANCER_INIT_POSITIONS = [(ORIGIN[0], ORIGIN[1]), (ORIGIN[0] + 1, ORIGIN[1]), 
                         (ORIGIN[0] - 1, ORIGIN[1]), (ORIGIN[0], ORIGIN[1] - 1), 
                         (ORIGIN[0], ORIGIN[1] + 1)]

# Initialize grid
def initialize_grid():
    M = np.full((ROWS, COLS), 'N')
    for pos in CANCER_INIT_POSITIONS:
        M[pos] = 'C'
    return M

# Function Definitions
def sum_cell_type(M, cell_type):
    """ Count number of a specific type of cell in the grid. """
    return np.sum(M == cell_type)

def mitosis_probability(k, n, p):
    """ Calculate probability of cell mitosis. """
    return k * (1 - n / p)

def origin_distance(r, c):
    """ Calculate grid distance from origin. """
    return math.sqrt((r - ORIGIN[0])**2 + (c - ORIGIN[1])**2)

def density_development(M):
    """ Calculate density development of tumor. """
    c = sum_cell_type(M, 'C')
    e = sum_cell_type(M, 'E')
    d = sum_cell_type(M, 'D')
    n_prime = c + e + d
    R = 0
    for i in range(ROWS):
        for j in range(COLS):
            if M[i, j] == 'C':
                R += origin_distance(i, j)
    R = R / n_prime if n_prime else 0
    return n_prime / R**2 if R else 0

def get_quadrant(r, c):
    """ Get quadrant of coordinates relative to origin. """
    if r <= ORIGIN[0] and c > ORIGIN[1]:
        return 'I'
    elif r <= ORIGIN[0] and c <= ORIGIN[1]:
        return 'II'
    elif r > ORIGIN[0] and c <= ORIGIN[1]:
        return 'III'
    else:
        return 'IV'

def mitosis(M, newM, r, c, dense):
    """ Model cell division with density development. """
    up, rt, dn, lt = (r-1, c), (r, c+1), (r+1, c), (r, c-1)
    quadrant = get_quadrant(r, c)
    dense_map = {'I': [up, rt], 'II': [lt, up], 'III': [dn, lt], 'IV': [rt, dn]}
    not_dense_map = {'I': [dn, lt], 'II': [rt, dn], 'III': [up, rt], 'IV': [lt, up]} 
    not_normal = ('E', 'D')
    map_choice = dense_map if dense else not_dense_map
    choices = map_choice[quadrant]
    
    for choice in choices:
        if newM[choice] not in not_normal:
            newM[choice] = 'C'
            break

def simulate_tumor_growth_one_generation(M):
    newM = np.copy(M)
    dense = density_development(M) > RHO
    for r in range(1, ROWS):
        for c in range(1, COLS):
            if M[r, c] == 'C':
                if random.random() < mitosis_probability(K1, sum_cell_type(M, 'C'), PHI):
                    mitosis(M, newM, r, c, dense)
                elif random.random() < K2:
                    newM[r, c] = 'E'
            elif M[r, c] == 'E' and random.random() < K3:
                newM[r, c] = 'D'
            elif M[r, c] == 'D' and random.random() < K4:
                newM[r, c] = 'N'

    return newM
