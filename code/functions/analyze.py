from functions.ca_model import *
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

def find_clusters(grid, ROWS, COLS):
    """
    Find clusters of 'C', cancer cells, in the given grid.

    Args:
    - grid: A numpy array representing the grid.
    - ROWS: Number of rows in the grid.
    - COLS: Number of columns in the grid.

    Returns: A list of sets, each set containing the coordinates of a cluster.
    """
    # Initialize a grid to keep track of visited cells
    visited = np.zeros_like(grid, dtype=bool)
    clusters = []

    # Traverse the grid
    for r in range(ROWS):
        for c in range(COLS):
            # If a cell contains 'C' and has not been visited, it's a new cluster
            if grid[r, c] == 'C' and not visited[r, c]:
                cluster = set()
                stack = [(r, c)]

                # Depth-first search to find all connected 'C' cells
                while stack:
                    current_r, current_c = stack.pop()
                    # Check bounds and if the cell is part of the cluster
                    if 0 <= current_r < ROWS and 0 <= current_c < COLS and grid[current_r, current_c] == 'C' and not visited[current_r, current_c]:
                        visited[current_r, current_c] = True
                        cluster.add((current_r, current_c))
                        # Add neighboring cells to the stack
                        stack.extend([(current_r + dr, current_c + dc) for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]])

                # If we found a cluster, add it to the list of clusters
                if cluster:
                    clusters.append(cluster)

    return clusters

# Assert statement for the find_clusters function
assert find_clusters(np.array([['N', 'C', 'C'], ['N', 'C', 'N'], ['N', 'N', 'N']]), 3, 3) == [{(0, 1), (0, 2), (1, 1)}], "The find_clusters function did not find the correct clusters."

def delay_coordinates_reconstruction(time_series, tau, d):
    """
    Reconstructs the delay coordinates from a time series.

    Args:
    - time_series: The time series data.
    - tau: The time delay.
    - d: The embedding dimension.

    Returns: The reconstructed delay coordinates.
    """
    n = len(time_series)
    # Ensure the time series is long enough for the given tau and d
    if n <= (d - 1) * tau:
        raise ValueError("Time series is too short for given tau and d values")

    # Construct the delay coordinates
    reconstructed = np.array([time_series[i:n - (d - 1 - i) * tau:tau] for i in range(d)])
    return reconstructed.T

# Convert cell types to numeric values for visualization
def cell_type_to_number(cell_type):
    """
    Converts a cell type character to a numeric value.

    Args:
    - Cell_type: The cell type character ('N', 'C', 'E', 'D').

    Returns: The numeric representation of the cell type.
    """
    return {'N': 0, 'C': 1, 'E': 2, 'D': 3}[cell_type]

def convert_matrix(M):
    """
    Converts a matrix of cell type characters to a matrix of numeric values.

    Args:
    - M: The matrix of cell type characters.

    Returns: The matrix of numeric values.
    """
    # Apply the cell_type_to_number conversion to the entire matrix
    numeric_M = np.vectorize(cell_type_to_number)(M)
    return numeric_M


def plot_simulate_tumor_growth(time_delay, generations, k1, k2):
    """
    Simulates tumor growth over a specified number of generations and plots the results every 20 generations.

    Args:
    - time_delay: Time delay factor in the simulation.
    - generations: Total number of generations to simulate.
    - k1: Proliferation rate of cancer cells.
    - k2: Inmune response rate against cancer cells.

    Returns: A history dictionary containing the state of the grid at each step.
    """
    # Assert that the necessary parameters are of the correct type
    assert isinstance(generations, int), "Generations parameter must be an integer"
    assert generations > 0, "Generations parameter must be positive"

    # Initialize history dictionary and simulation grid
    history = {}
    M = initialize_grid()

    # Set up the plot
    plt.figure(figsize=(20, 8))
    iteration_numbers = []  # Track the number of iterations
    plot_count = 0  # Count how many plots have been made

    # Iterate over each generation to simulate tumor growth
    for g in range(generations):
        iteration_numbers.append(g)
        M = simulate_tumor_growth_one_step(M, g, time_delay, history, k1, k2)

        # Plot the grid every 20 generations
        if g % 20 == 0:
            plot_count += 1
            plt.subplot(1, min(5, generations // 20), plot_count)
            plt.imshow(convert_matrix(M), cmap=ListedColormap(['white', 'black', 'red', 'green']))
            plt.title(f'Generation {g}')
            plt.axis('off')

            # If we have plotted 5 times, show the plot and reset for new figure
            if plot_count == 5:
                plt.show()
                plt.figure(figsize=(20, 8))
                plot_count = 0

    # Show the final plot
    plt.show()

    return history

def simulate_and_find_metastasis(generations, rows, cols, k1, k2):

    ORIGIN = (cols // 2, rows // 2)
    CANCER_INIT_POSITIONS = [(ORIGIN[0], ORIGIN[1]), (ORIGIN[0] + 1, ORIGIN[1]),
                            (ORIGIN[0] - 1, ORIGIN[1]), (ORIGIN[0], ORIGIN[1] - 1),
                            (ORIGIN[0], ORIGIN[1] + 1)]

    M = initialize_grid(rows, cols, CANCER_INIT_POSITIONS)
    num_clusters_list = []
    Tm = None

    for g in range(generations):
        M = simulate_tumor_growth_one_step_metastasis(M, k1, k2, rows, cols, ORIGIN)
        clusters = find_clusters(M, rows, cols)
        num_clusters = len(clusters)
        num_clusters_list.append(len(clusters))
        
        if num_clusters > 50 and Tm is None:
            Tm = g

    return num_clusters_list, Tm
