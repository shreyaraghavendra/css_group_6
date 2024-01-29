import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import math
import random
import csv

RANDOM_SEED = 42
random.seed(RANDOM_SEED)

def initialize_grid(rows, cols, cancer_init_positions):
    M = np.full((rows, cols), 'N')
    for pos in cancer_init_positions:
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

def origin_distance(M, origin):
    n_prime = calculate_n_prime(M)
    R = 0
    for i in range(len(M)):
        for j in range(len(M[0])):
            if M[i, j] == 'C':
                R += math.sqrt((i - origin[0])**2 + (j - origin[1])**2)
    R = R / n_prime if n_prime else 0
    return R

def density_development(M, origin):
    """ Calculate density development of tumor. """
    n_prime = calculate_n_prime(M)
    R = origin_distance(M, origin)
    return n_prime / R**2 if R else 0

def mitosis_probability(k, n, p, time_delay, generation, history):
    delayed_gen = generation - time_delay
    if delayed_gen in history:
        n_delayed = history[delayed_gen]['Nc']
        return k * (1 - n_delayed / p)
    else:
        return k * (1 - n / p)

def store_history(generation, M, history, origin, RHO):
    """ Store the number of each cell type and R at the current generation. """
    Nc = sum_cell_type(M, 'C')
    Ne = sum_cell_type(M, 'E')
    Nd = sum_cell_type(M, 'D')
    R = origin_distance(M, origin)  # Calculate radius here
    dense = (density_development(M, origin) > RHO)
    history[generation] = {'Nc': Nc, 'Ne': Ne, 'Nd': Nd, 'R': R, "dense": dense}

def get_quadrant(r, c, ORIGIN):
    """ Get quadrant of coordinates relative to origin. """
    if r <= ORIGIN[0] and c > ORIGIN[1]:
        return 'I'
    elif r <= ORIGIN[0] and c <= ORIGIN[1]:
        return 'II'
    elif r > ORIGIN[0] and c <= ORIGIN[1]:
        return 'III'
    else:
        return 'IV'

def mitosis(M, newM, r, c, dense, ORIGIN):
    """ Model cell division with density development. """
    up, rt, dn, lt = (r-1, c), (r, c+1), (r+1, c), (r, c-1)
    quadrant = get_quadrant(r, c, ORIGIN)
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

def find_clusters(grid, ROWS,COLS):
    visited = np.zeros_like(grid, dtype=bool)
    clusters = []

    for r in range(ROWS):
        for c in range(COLS):
            if grid[r, c] == 'C' and not visited[r, c]:
                cluster = set()
                stack = [(r, c)]

                while stack:
                    current_r, current_c = stack.pop()
                    if 0 <= current_r < ROWS and 0 <= current_c < COLS and grid[current_r, current_c] == 'C' and not visited[current_r, current_c]:
                        visited[current_r, current_c] = True
                        cluster.add((current_r, current_c))
                        stack.extend([(current_r + dr, current_c + dc) for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]])

                if cluster:
                    clusters.append(cluster)

    return clusters

def simulate_tumor_growth_one_step(M, generation, time_delay, history, phi, rho, k1, k2, k3, k4, origin, rows, cols):
    newM = np.copy(M)
    store_history(generation, M, history, origin, rho)
    dense = history[generation]['dense']

    delayed_gen = generation - time_delay
    if delayed_gen in history:
        dense = history[delayed_gen]['dense']
    
    for r in range(1, rows-1):
        for c in range(1, cols-1):
            if M[r, c] == 'C':
                mitosis_prob = mitosis_probability(k1, sum_cell_type(M, 'C'), phi, time_delay, generation, history)
                if random.random() < mitosis_prob:
                    newM = mitosis(M, newM, r, c, dense, origin)
                elif random.random() < k2:
                    newM[r, c] = 'E'
            elif M[r, c] == 'E' and random.random() < k3:
                newM[r, c] = 'D'
            elif M[r, c] == 'D' and random.random() < k4:
                newM[r, c] = 'N'
    return newM

def simulate_tumor_growth(time_delay, generations, rows, cols, phi, rho, k1, k2, k3, k4, cancer_init_positions, origin):
    history = {}
    M = initialize_grid(rows, cols, cancer_init_positions)

    for g in range(generations):
        M = simulate_tumor_growth_one_step(M, g, time_delay, history, phi, rho, k1, k2, k3, k4, origin, rows, cols)

    return history

def simulate_tumor_growth_with_clusters(time_delay, generations, rows, cols, phi, rho, k1, k2, k3, k4, cancer_init_positions, origin):
    history = {}
    M = initialize_grid(rows, cols, cancer_init_positions)
    M_cluster = []

    for g in range(generations):
        M = simulate_tumor_growth_one_step(M, g, time_delay, history, phi, rho, k1, k2, k3, k4, origin, rows, cols)

        M_cluster.append(M)

    return history, M_cluster

# create delay array
def delay_coordinates_reconstruction(time_series, tau, d):
    n = len(time_series)
    if n <= (d - 1) * tau:
        raise ValueError("Time series is too short for given tau and d values")

    reconstructed = np.array([time_series[i:n - (d - 1 - i) * tau:tau] for i in range(d)])
    return reconstructed.T


# visualizing simulation functions
def cell_type_to_number(cell_type):
    return {'N': 0, 'C': 1, 'E': 2, 'D': 3}[cell_type]

def convert_matrix(M):
    numeric_M = np.vectorize(cell_type_to_number)(M)
    return numeric_M

def plot_simulate_tumor_growth(time_delay, generations, rows, cols, phi, rho, k1, k2, k3, k4, cancer_init_positions, origin):
    history = {}
    M = initialize_grid(rows, cols, cancer_init_positions)

    plt.figure(figsize=(20, 8))
    iteration_numbers = []
    plot_count = 0

    for g in range(generations):
        iteration_numbers.append(g)
        M = simulate_tumor_growth_one_step(M, g, time_delay, history, phi, rho, k1, k2, k3, k4, origin, rows, cols)
        if g % 20 == 0:
            plot_count += 1
            plt.subplot(1, min(5, generations // 20), plot_count)
            plt.imshow(convert_matrix(M), cmap=ListedColormap(['white', 'black', 'red', 'green']))
            plt.title(f'Generation {g}')
            plt.axis('off')

            if plot_count == 5:
                plt.show()
                plt.figure(figsize=(20, 8))
                plot_count = 0
    plt.show()
    return history

def read_history(history_array, history_csv_file = 'history_data.csv'):
    """
        #it is used in this way:
        history_csv_file = '../data/history_data.csv'
        history_array = []
        history_array = read_history(history_array, history_csv_file)
        for tau in range(0, 100):
        for g in range(0, GENERATIONS):
            print(history_array[tau][g])
    """
    # Read the CSV file and store the data in groups of 500 lines
    with open(history_csv_file, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        group = []
        for i, row in enumerate(reader):
            group.append(row)
            # Add to the history array and reset the group after accumulating 500 lines, or at the end of the file
            if (i + 1) % 500 == 0 or i == reader.line_num - 1:
                history_array.append(group)
                group = []
    print(f"Importing completed, there are {len(history_array)} history entries in total")
    return history_array

def read_matrix(all_M, generation, matrices_csv_file = 'matrices_data.csv'):
    """
        #it is used in this way:
        matrices_csv_file = '../data/matrices_data.csv'
        all_M = []
        all_M = read_matrix(all_M, GENERATIONS, matrices_csv_file)
        for tau in range(0, 100):
        for g in range(0, GENERATIONS):
            print(all_M[tau][g])
    """
    
    def reconstruct_matrix(row, rows, cols):
        # Convert the row to a NumPy array and reshape it back to the original matrix shape
        return np.array(row).reshape(rows, cols)

    all_M = []
    # Read the CSV file
    with open(matrices_csv_file, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)

        M_for_tau = []

        # Iterate over each row and reconstruct the matrix
        for row in reader:
            M = reconstruct_matrix(row, ROWS, COLS)
            M_for_tau.append(M)
            if len(M_for_tau) == GENERATIONS:
                all_M.append(M_for_tau.copy())
                M_for_tau = []

    # Now, reconstructed_matrices contains all the 2D matrices
    print(f"Total tau reconstructed: {len(all_M)}")
    return all_M
