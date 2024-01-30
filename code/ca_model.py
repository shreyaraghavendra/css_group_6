import numpy as np
import math
import random

RANDOM_SEED = 42
random.seed(RANDOM_SEED)

ROWS = COLS = 101
ORIGIN = (COLS // 2, ROWS // 2)
PHI = 1000
CANCER_INIT_POSITIONS = [(ORIGIN[0], ORIGIN[1]), (ORIGIN[0] + 1, ORIGIN[1]),
                         (ORIGIN[0] - 1, ORIGIN[1]), (ORIGIN[0], ORIGIN[1] - 1),
                         (ORIGIN[0], ORIGIN[1] + 1)]
K3, K4 = 0.4, 0.4
RHO = 3.85

def initialize_grid():
    M = np.full((ROWS, COLS), 'N')
    for pos in CANCER_INIT_POSITIONS:
        M[pos] = 'C'
    return M


def sum_cell_type(M, cell_type):
    """ Count number of a specific type of cell in the grid. """
    return np.sum(M == cell_type)


def calculate_n_prime(M):
    c = sum_cell_type(M, 'C')
    e = sum_cell_type(M, 'E')
    d = sum_cell_type(M, 'D')
    n_prime = c + e + d
    return n_prime


def origin_distance(M):
    n_prime = calculate_n_prime(M)
    R = 0
    for i in range(len(M)):
        for j in range(len(M[0])):
            if M[i, j] == 'C':
                R += math.sqrt((i - ORIGIN[0]) ** 2 + (j - ORIGIN[1]) ** 2)
    R = R / n_prime if n_prime else 0
    return R


def density_development(M):
    """ Calculate density development of tumor. """
    n_prime = calculate_n_prime(M)
    R = origin_distance(M)
    return n_prime / R ** 2 if R else 0


def mitosis_probability(k, n, time_delay, generation, history):
    delayed_gen = generation - time_delay
    if delayed_gen in history:
        n_delayed = history[delayed_gen]['Nc']
        return k * (1 - n_delayed / PHI)
    else:
        return k * (1 - n / PHI)


def store_history(generation, M, history):
    """ Store the number of each cell type and R at the current generation. """
    Nc = sum_cell_type(M, 'C')
    Ne = sum_cell_type(M, 'E')
    Nd = sum_cell_type(M, 'D')
    R = origin_distance(M)  # Calculate radius here
    dense = (density_development(M) > RHO)
    history[generation] = {'Nc': Nc, 'Ne': Ne, 'Nd': Nd, 'R': R, "dense": dense}


def get_quadrant(r, c):
    """ Get quadrant of coordinates relative to ORIGIN. """
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
    up, rt, dn, lt = (r - 1, c), (r, c + 1), (r + 1, c), (r, c - 1)
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
    return newM

def simulate_tumor_growth_one_step(M, generation, time_delay, history, k1, k2):
    newM = np.copy(M)
    store_history(generation, M, history)
    dense = history[generation]['dense']

    delayed_gen = generation - time_delay
    if delayed_gen in history:
        dense = history[delayed_gen]['dense']

    for r in range(1, ROWS - 1):
        for c in range(1, COLS - 1):
            if M[r, c] == 'C':
                mitosis_prob = mitosis_probability(k1, sum_cell_type(M, 'C'), time_delay, generation, history)
                if random.random() < mitosis_prob:
                    newM = mitosis(M, newM, r, c, dense)
                elif random.random() < k2:
                    newM[r, c] = 'E'
            elif M[r, c] == 'E' and random.random() < K3:
                newM[r, c] = 'D'
            elif M[r, c] == 'D' and random.random() < K4:
                newM[r, c] = 'N'
    return newM


def simulate_tumor_growth(time_delay, generations, k1, k2):
    history = {}
    M = initialize_grid()

    for g in range(generations):
        M = simulate_tumor_growth_one_step(M, g, time_delay, history, k1, k2)

    return history

def simulate_tumor_growth_with_clusters(time_delay, generations, k1, k2):
    history = {}
    M = initialize_grid()
    M_cluster = []

    for g in range(generations):
        M = simulate_tumor_growth_one_step(M, g, time_delay, history, k1, k2)

        M_cluster.append(M)

    return history, M_cluster