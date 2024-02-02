import numpy as np
import csv

def read_history(history_array, history_csv_file='history_data.csv'):
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


def read_matrix(rows, cols, all_M, generation, matrices_csv_file='matrices_data.csv'):
    """
        #it is used in this way:
        matrices_csv_file = '../data/matrices_data.csv'
        ROWS = 101
        COLS = 101
        all_M = []
        all_M = read_matrix(ROWS, COLS, all_M, GENERATIONS, matrices_csv_file)
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
            M = reconstruct_matrix(row, rows, cols)
            M_for_tau.append(M)
            if len(M_for_tau) == generation:
                all_M.append(M_for_tau.copy())
                M_for_tau = []

    # Now, reconstructed_matrices contains all the 2D matrices
    print(f"Total tau reconstructed: {len(all_M)}")
    return all_M