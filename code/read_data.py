import numpy as np
import csv

def read_history(history_array, history_csv_file='history_data.csv'):
    """
    The function reads the history data from the CSV file and stores it in the history_array.

    Args:
        - history_array: the array to store the history data.
        - history_csv_file: the path to the CSV file.
  
    Returns: The array containing the history data.
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
    The function reads the matrices from the CSV file and stores them in the all_M array.

    Args:
        - rows: the number of rows in the matrix.
        - cols: the number of columns in the matrix.
        - all_M: the array to store the matrices.
        - generations: the number of generations.
        - matrices_csv_file: the path to the CSV file.

    Returns: The array containing the matrices.
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