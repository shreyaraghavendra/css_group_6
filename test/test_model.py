import inspect
import json
import random
import pytest
import numpy as np
from code.functions.ca_model import simulate_tumor_growth, simulate_tumor_growth_with_clusters


def compare_outputs(actual_output, expected_output):
    """
    Compares the actual output with the expected output, suitable for complex data structures.

    Parameters:
    - actual_output: The actual output from the function.
    - expected_output: The expected output to compare against.

    Returns:
    - A tuple of (boolean, message) indicating whether the outputs match and a descriptive message.
    """
    if isinstance(actual_output, dict) and isinstance(expected_output, dict):
        for key, expected_val in expected_output.items():
            if key not in actual_output:
                return False, f"Key '{key}' not found in actual output."
            actual_val = actual_output[key]
            if isinstance(expected_val, (list, np.ndarray)) and isinstance(actual_val, (list, np.ndarray)):
                if not np.allclose(np.array(actual_val), np.array(expected_val)):
                    return False, f"Value mismatch for key: {key}. Expected: {expected_val}, Actual: {actual_val}"
            else:
                if actual_val != expected_val:
                    return False, f"Value mismatch for key: {key}. Expected: {expected_val}, Actual: {actual_val}"
    else:
        # Assuming the output is a tuple with a list (of cancer cell grids) as its second element
        cancer_cell_grid = actual_output[1][0].tolist()
        if cancer_cell_grid != expected_output[1][0]:
            return False, f"actual_output[1]: {actual_output[1]}, expected_output[1]: {expected_output[1]}"
        return compare_outputs(actual_output[0], expected_output[0])
    return True, "Outputs match."


def test_simulate_tumor_growth_with_stored_data():
    """
    Tests the simulate_tumor_growth function with data stored in a JSON file.
    """
    data_file_path = "data/simulate_tumor_growth_data.json"
    with open(data_file_path, 'r') as file:
        data = json.load(file)

    for item in data:
        output = item['output']
        new_output = {int(k): v for k, v in output.items()}
        item['output'] = new_output

    for item in data:
        input_data = item['input']
        expected_output = item['output']

        sig = inspect.signature(simulate_tumor_growth)
        relevant_args = {k: v for k, v in input_data.items() if k in sig.parameters}
        random.seed(42)
        actual_output = simulate_tumor_growth(**relevant_args)
        comparison_result, message = compare_outputs(actual_output, expected_output)

        assert comparison_result, message


def test_simulate_tumor_growth_with_clusters():
    """
    Tests the simulate_tumor_growth_with_clusters function with data stored in a JSON file.
    """
    data_file_path = "data/simulate_tumor_growth_with_clusters.json"
    with open(data_file_path, 'r') as file:
        data = json.load(file)

    for item in data:
        output = item['output'][0]
        new_output = {int(k): v for k, v in output.items()}
        item['output'][0] = new_output

    for item in data:
        input_data = item['input']
        expected_output = item['output']

        sig = inspect.signature(simulate_tumor_growth_with_clusters)
        relevant_args = {k: v for k, v in input_data.items() if k in sig.parameters}
        random.seed(42)
        actual_output = simulate_tumor_growth_with_clusters(**relevant_args)
        comparison_result, message = compare_outputs(actual_output, expected_output)

        assert comparison_result, message
