import numpy as np
import math
import random

# Set a random seed for reproducibility
RANDOM_SEED = 42
random.seed(RANDOM_SEED)

# Define grid dimensions and initial parameters
ROWS = COLS = 101
ORIGIN = (COLS // 2, ROWS // 2)
PHI = 1000
CANCER_INIT_POSITIONS = [(ORIGIN[0], ORIGIN[1]), (ORIGIN[0] + 1, ORIGIN[1]),
                         (ORIGIN[0] - 1, ORIGIN[1]), (ORIGIN[0], ORIGIN[1] - 1),
                         (ORIGIN[0], ORIGIN[1] + 1)]
K3, K4 = 0.4, 0.4  # Define mitosis and apoptosis probabilities
RHO = 3.85  # Define a threshold for density development

def initialize_grid(ROWS=ROWS, COLS=COLS, CANCER_INIT_POSITIONS=CANCER_INIT_POSITIONS):
    """Initialize the grid with normal cells and initial cancer cells."""
    M = np.full((ROWS, COLS), 'N')
    for pos in CANCER_INIT_POSITIONS:
        M[pos] = 'C'
    return M

# def initialize_grid():
#     """Initialize the grid with normal cells and initial cancer cells."""

#     M = np.full((ROWS, COLS), 'N')
#     for pos in CANCER_INIT_POSITIONS:
#         M[pos] = 'C'
#     return M

def sum_cell_type(M, cell_type):
    """
    Count the number of a specific cell type in the grid.

    Args:
        - M: The grid of cells.
        - cell_type: The type of cell to count.

    Returns: The number of cells of the specified type.
    """
    return np.sum(M == cell_type)

def calculate_n_prime(M):
    """
    Calculate the total number of cancerous, edge, and dead cells.
    
    Args:
        - M: The grid of cells.

    Returns: The total number of cells; C + E + D.
    """
    c = sum_cell_type(M, 'C')
    e = sum_cell_type(M, 'E')
    d = sum_cell_type(M, 'D')
    n_prime = c + e + d
    return n_prime

def origin_distance(M, ORIGIN=ORIGIN):
    """
    Calculate the average distance of cancer cells from the origin.

    Args:
        - M: The grid of cells.

    Returns: The distance of cancer cells from the origin.
    """
    n_prime = calculate_n_prime(M)
    R = 0
    for i in range(len(M)):
        for j in range(len(M[0])):
            if M[i, j] == 'C':
                R += math.sqrt((i - ORIGIN[0]) ** 2 + (j - ORIGIN[1]) ** 2)
    R = R / n_prime if n_prime else 0
    return R

def density_development(M, ORIGIN=ORIGIN):
    """
    Calculate the density development of the tumor.

    Args:
        - M: The grid of cells.

    Returns: The density development of the tumor.
    """
    n_prime = calculate_n_prime(M)
    R = origin_distance(M)
    return n_prime / R ** 2 if R else 0

def basic_mitosis_probability(k, n):
    """Calculate the probability of a cell undergoing mitosis."""
    return k * (1 - n / PHI)

def mitosis_probability(k1, n, time_delay, generation, history):
    """
    Calculate the probability of a cell undergoing mitosis.

    Args:
        - k1: Proliferation rate of cancer cells.
        - n: The number of cancerous cells.
        - time_delay: The time delay.
        - generation: The current generation of the simulation.
        - history: A record of the previous states of the simulation.

    Returns: The probability of a cell undergoing mitosis.
    """
    delayed_gen = generation - time_delay
    if delayed_gen in history:
        n_delayed = history[delayed_gen]['Nc']
        return k1 * (1 - n_delayed / PHI)
    else:
        return k1 * (1 - n / PHI)


def store_history(generation, M, history):
    """ 
    Store the number of each cell type and R at the current generation. 
    
    Args:
        - generation: The current generation of the simulation.
        - M: The grid of cells.
        - history: A record of the previous states of the simulation.
    
    """
    Nc = sum_cell_type(M, 'C')
    Ne = sum_cell_type(M, 'E')
    Nd = sum_cell_type(M, 'D')
    R = origin_distance(M)  # Calculate radius here
    dense = (density_development(M) > RHO)
    history[generation] = {'Nc': Nc, 'Ne': Ne, 'Nd': Nd, 'R': R, "dense": dense}


def get_quadrant(r, c):
    """
    Get quadrant of coordinates relative to ORIGIN.
    
    Args:
        - r: The row index of the cell.
        - c: The column index of the cell.

    Returns: The quadrant of the cell.
    """
    if r <= ORIGIN[0] and c > ORIGIN[1]:
        return 'I'
    elif r <= ORIGIN[0] and c <= ORIGIN[1]:
        return 'II'
    elif r > ORIGIN[0] and c <= ORIGIN[1]:
        return 'III'
    else:
        return 'IV'


def mitosis(M, newM, r, c, dense):
    """
    Model the cell division process, considering the tumor density development.

    Args:
        - M: The current state of the grid.
        - newM: The grid for the next state.
        - r: The row index of the dividing cell.
        - c: The column index of the dividing cell.
        - dense: A boolean indicating whether the tumor is dense or not.

    Returns: The updated grid, newM, with the result of the division.
    """
    # Define directions relative to the cell position
    up, rt, dn, lt = (r - 1, c), (r, c + 1), (r + 1, c), (r, c - 1)
    # Get the quadrant to determine division direction
    quadrant = get_quadrant(r, c)
    # Maps for cell division based on tumor density
    dense_map = {'I': [up, rt], 'II': [lt, up], 'III': [dn, lt], 'IV': [rt, dn]}
    not_dense_map = {'I': [dn, lt], 'II': [rt, dn], 'III': [up, rt], 'IV': [lt, up]}
    # Exclude cells that are not normal for division
    not_normal = ('E', 'D')
    # Choose the appropriate map based on density
    map_choice = dense_map if dense else not_dense_map
    choices = map_choice[quadrant]

    # Attempt to divide the cell in the chosen directions
    for choice in choices:
        if newM[choice] not in not_normal:
            newM[choice] = 'C'
            break
    return newM


# Assert statement to check if the mitosis function returns a numpy array
assert isinstance(mitosis(np.array([['N', 'N'], ['N', 'N']]), np.array([['N', 'N'], ['N', 'N']]), 0, 0, False), np.ndarray), "Mitosis function must return a numpy array"


def simulate_tumor_growth_one_step(M, generation, time_delay, history, k1, k2):
    """
    Simulate a single step of tumor growth in the cellular automaton.

    Args:
        - M: Current state of the grid.
        - generation: Current generation of the simulation.
        - time_delay: Time delay factor for mitosis probability calculation.
        - history: A record of the previous states of the simulation.
        - k1: Proliferation rate of cancer cells.
        - k2: Inmune response rate against cancer cells.

    Returns: The grid, newM, after one step of simulation.
    """
    newM = np.copy(M)  # Create a copy of the grid for the new state
    store_history(generation, M, history)  # Store the current state in history
    dense = history[generation]['dense']  # Determine if current state is dense

    # Check for time delay effect on density
    delayed_gen = generation - time_delay
    if delayed_gen in history:
        dense = history[delayed_gen]['dense']

    # Iterate over the grid to simulate cell behavior
    for r in range(1, ROWS - 1):
        for c in range(1, COLS - 1):
            if M[r, c] == 'C':
                # Calculate mitosis probability for cancerous cells
                mitosis_prob = mitosis_probability(k1, sum_cell_type(M, 'C'), time_delay, generation, history)
                if random.random() < mitosis_prob:
                    # Perform mitosis if probability threshold is met
                    newM = mitosis(M, newM, r, c, dense)
                elif random.random() < k2:
                    # Change cell state to 'E' if probability threshold is met
                    newM[r, c] = 'E'
            elif M[r, c] == 'E' and random.random() < K3:
                # Change cell state to 'D' for 'E' cells
                newM[r, c] = 'D'
            elif M[r, c] == 'D' and random.random() < K4:
                # Change cell state to 'N' for 'D' cells
                newM[r, c] = 'N'
    return newM


# Sample assert statement to ensure function returns a numpy array
assert isinstance(simulate_tumor_growth_one_step(np.full((ROWS, COLS), 'N'), 0, 1, {}, 0.1, 0.2),
                  np.ndarray), "Function must return a numpy array"

def simulate_tumor_growth_one_step_metastasis(M, k1, k2, ROWS, COLS, ORIGIN):
  
    newM = np.copy(M)
    dense = (density_development(M,ORIGIN) > RHO)

    for r in range(1, ROWS - 1):
        for c in range(1, COLS - 1):
            if M[r, c] == 'C':
                mitosis_prob = basic_mitosis_probability(k1, sum_cell_type(M, 'C'))
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
    """
    Simulate the growth of a tumor over multiple generations.

    Args:
        - time_delay: Time delay factor for mitosis probability calculation.
        - generations: Number of generations to simulate.
        - k1: Proliferation rate of cancer cells.
        - k2: Inmune response rate against cancer cells.

    Returns: A dictionary named history recording the state of the simulation at each generation.
    """
    history = {}  # Initialize history record
    M = initialize_grid()  # Initialize the grid

    # Simulate growth over the specified number of generations
    for g in range(generations):
        M = simulate_tumor_growth_one_step(M, g, time_delay, history, k1, k2)

    # Return the history of the simulation
    return history


# Sample assert statement to ensure function returns a dictionary
assert isinstance(simulate_tumor_growth(1, 10, 0.1, 0.2), dict), "Function must return a dictionary"


def simulate_tumor_growth_with_clusters(time_delay, generations, k1, k2):
    """
    Simulate the tumor growth over a number of generations with cluster tracking.

    Args:
        - time_delay: The delay in generations for mitosis to affect tumor density.
        - generations: The total number of generations to simulate.
        - k1: Proliferation rate of cancer cells.
        - k2: Inmune response rate against cancer cells.

    Returns: Tuple of history (dict) of tumor growth and cancer_cell_grid (list) of numpy arrays representing tumor state at each generation.
    """
    # Initialize history dictionary and the grid
    history = {}
    M = initialize_grid()
    # List to store the grid state at each generation for clusters
    cancer_cell_grid= []


    # Iterate over each generation to simulate tumor growth
    for g in range(generations):
        # Simulate one step of tumor growth
        M = simulate_tumor_growth_one_step(M, g, time_delay, history, k1, k2)
        # Append the state of the grid to cancer_cell_grid
        cancer_cell_grid.append(M)

    # Assert statements to verify the correctness of the simulation's output
    assert isinstance(history, dict), "History must be a dictionary"
    assert all(isinstance(M, np.ndarray) for M in cancer_cell_grid), "All elements in cancer_cell_grid must be numpy arrays"
    assert len(cancer_cell_grid) == generations, "The length of cancer_cell_grid must be equal to the number of generations"

    # Additional assert statement to check if history contains expected keys
    expected_keys = {'Nc', 'Ne', 'Nd', 'R', 'dense'}
    assert all(key in history[0] for key in expected_keys), "History should contain expected keys for simulation data"

    return history, cancer_cell_grid