from ca_model import *
import matplotlib.pyplot as plt

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