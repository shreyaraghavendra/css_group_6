
import code.ca_model as ca
from code.analyze import *
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


from ipywidgets import interact, interactive, fixed, interact_manual
import ipywidgets as widgets
from matplotlib.widgets import Slider


# # %%
# def simulate_tumor_growth(time_delay, generations, rows, cols, phi, rho, k1, k2, k3, k4, cancer_init_positions, origin):
#     history = {}
#     M = ca.initialize_grid(rows, cols, cancer_init_positions)
#     M_cluster = []

#     for g in range(generations):
#         M = ca.simulate_tumor_growth_one_step(M, g, time_delay, history, phi, rho, k1, k2, k3, k4, origin, rows, cols)

#         M_cluster.append(M)

#     return history, M_cluster

# %%
GENERATIONS = 500
ROWS = COLS = 101
ORIGIN = (COLS // 2, ROWS // 2)
PHI = 1000
CANCER_INIT_POSITIONS = [(ORIGIN[0], ORIGIN[1]), (ORIGIN[0] + 1, ORIGIN[1]), 
                         (ORIGIN[0] - 1, ORIGIN[1]), (ORIGIN[0], ORIGIN[1] - 1), 
                         (ORIGIN[0], ORIGIN[1] + 1)]
K2, K3, K4 = 0.2, 0.4, 0.4
RHO = 3.85

TIME_DELAY = 50
NO_TIME_DELAY = 0





K1_values = [0.9]  # Use only k1=0.9 for this example
# tau_values = [1, 49]  # Specify tau values of interest
tau_values = [1]

# Initial generation
initial_generation = 0



for i, K1 in enumerate(K1_values):
    for tau in tau_values:
        fig, ax = plt.subplots(figsize=(15, 6))
        plt.subplots_adjust(bottom=0.25)  # Adjust the bottom margin to make room for the slider
        fig.suptitle(f'Grid Visualization of Cancer Cell Clusters for K1={K1}, tau={tau}')

        history, Ms = simulate_tumor_growth(tau, GENERATIONS, K1, K2)
      
        # Initial grid
        clusters = find_clusters(Ms[initial_generation], ROWS, COLS)
        cluster_sizes = [len(cluster) for cluster in clusters]
        grid = np.zeros((ROWS, COLS))

        for idx, cluster in enumerate(clusters):
            for cell in cluster:
                row, col = cell
                grid[row, col] = cluster_sizes[idx]

        img = ax.imshow(grid, cmap='viridis', interpolation='nearest')
        ax.set_title(f'Generation {initial_generation + 1}')
        ax.axis('off')

        # Add a slider for selecting generations
        ax_slider = plt.axes([0.25, 0.1, 0.65, 0.03], facecolor='lightgoldenrodyellow')
        generation_slider = Slider(ax_slider, 'Generation', 1, GENERATIONS, valinit=initial_generation + 1, valstep=1)

        def update(val):
            generation = int(generation_slider.val) - 1
            clusters = find_clusters(Ms[generation], ROWS, COLS)
            cluster_sizes = [len(cluster) for cluster in clusters]

            grid = np.zeros((ROWS, COLS))
            for idx, cluster in enumerate(clusters):
                for cell in cluster:
                    row, col = cell
                    grid[row, col] = cluster_sizes[idx]

            img.set_array(grid)
            ax.set_title(f'Generation {generation + 1}')
            fig.canvas.draw_idle()

        generation_slider.on_changed(update)
    plt.show()





