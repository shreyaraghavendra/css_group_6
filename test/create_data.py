import inspect
import json
import random
import numpy
from code.functions.ca_model import *  # Importing all from a custom model module
import numpy as np

# Setting a fixed seed for reproducibility
random.seed(42)
numpy.random.seed(42)


def custom_serializer(obj):
    """
    Custom serializer function to handle types that cannot be directly serialized.

    Parameters:
    - obj: The object to serialize.

    Returns:
    - Serializable representation of `obj`.
    """
    if isinstance(obj, np.ndarray):
        return obj.tolist()  # Convert NumPy arrays to list
    elif isinstance(obj, (np.int_, np.intc, np.intp, np.int8,
                          np.int16, np.int32, np.int64,
                          np.uint8, np.uint16, np.uint32, np.uint64)):
        return int(obj)  # Convert NumPy integers to Python int
    elif isinstance(obj, (np.float_, np.float16, np.float32, np.float64)):
        return float(obj)  # Convert NumPy floats to Python float
    elif isinstance(obj, (np.complex_, np.complex64, np.complex128)):
        return {'real': obj.real, 'imag': obj.imag}  # Convert NumPy complex numbers to dictionary
    elif isinstance(obj, (np.bool_)):
        return bool(obj)  # Convert NumPy boolean to Python bool
    elif hasattr(obj, '__dict__'):
        return obj.__dict__  # Attempt to convert object to its attribute dictionary
    else:
        raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")


def generate_random_args(model_module):
    """
    Generates random input data for a given model module.

    Parameters:
    - model_module: The module containing the model function to generate inputs for.

    Returns:
    - A tuple containing the input data dictionary and a dictionary of relevant arguments for the model.
    """
    input_data = {
        'time_delay': random.randint(1, 10),
        'generations': random.randint(50, 100),
        'rows': random.randint(50, 100),
        'cols': random.randint(50, 100),
        'phi': random.randint(100, 200),
        'rho': random.uniform(0.1, 0.9),
        'k1': random.uniform(0.1, 0.9),
        'k2': random.uniform(0.1, 0.9),
        'k3': random.uniform(0.1, 0.9),
        'k4': random.uniform(0.1, 0.9),
        'cancer_init_positions': [(random.randint(25, 75), random.randint(25, 75)) for _ in range(5)],
        'origin': (50, 50)
    }

    sig = inspect.signature(model_module)
    relevant_args = {k: v for k, v in input_data.items() if k in sig.parameters}
    return input_data, relevant_args


def generate_and_store_multiple_data_sets(model_module, output_file_path, num_sets=5):
    """
    Generates multiple sets of data for a given model, simulates the model, and stores the input and output data in a JSON file.

    Parameters:
    - model_module: The module containing the model function.
    - output_file_path: The path to the file where the data will be stored.
    - num_sets: The number of data sets to generate and store.
    """
    random.seed(42)
    all_data = []  # List to store multiple sets of data

    for _ in range(num_sets):
        input_data, relevant_args = generate_random_args(model_module)
        random.seed(42)
        output_data = model_module(**relevant_args)  # Simulate model function and get output data

        all_data.append({
            'input': input_data,
            'output': output_data  # Add current set of input and output to the list
        })

    with open(output_file_path, 'w') as f:
        json.dump(all_data, f, indent=4, default=custom_serializer)  # Store all sets of data in a JSON file


def read_data_and_compare_with_function_output(json_file_path, function, **function_args):
    """
    Reads data from a JSON file and compares it with the output of a given function.

    This function is intended to validate the correctness of the function's output
    by comparing it against expected output stored in a JSON file.

    Parameters:
    - json_file_path: Path to the JSON file containing input and expected output data.
    - function: The function to test.
    - **function_args: Additional arguments to pass to the function (if any).
    """
    with open(json_file_path, 'r') as file:
        data = json.load(file)

    for item in data:
        input_data = item['input']
        expected_output = item['output']

        sig = inspect.signature(function)
        relevant_args = {k: v for k, v in input_data.items() if k in sig.parameters}
        random.seed(42)
        actual_output = function(**relevant_args)

        if not isinstance(actual_output, dict):
            print("Actual output is not a dictionary. Please check the function's return type.")
            continue

        for key, expected_val in expected_output.items():
            if key not in actual_output:
                print(f"Key '{key}' not found in actual output.")
                continue

            actual_val = actual_output[key]
            if isinstance(expected_val, list):  # Assuming lists represent NumPy arrays
                expected_val = np.array(expected_val)
                comparison_result = np.array_equal(actual_val, expected_val)
            else:
                comparison_result = actual_val == expected_val

            if comparison_result:
                print(f"Output matches for key: {key}.")
            else:
                print(f"Output does not match for key: {key}. Expected: {expected_val}, Actual: {actual_val}")


num_sets = 4  # Set the number of data sets to generate

# Data generation for the simulate_tumor_growth function
file_simulate_tumor_growth = "data/simulate_tumor_growth_data.json"
generate_and_store_multiple_data_sets(simulate_tumor_growth, file_simulate_tumor_growth, num_sets)
read_data_and_compare_with_function_output(file_simulate_tumor_growth, simulate_tumor_growth)

# Data generation for the simulate_tumor_growth_with_clusters function
file_simulate_tumor_growth_with_clusters = "data/simulate_tumor_growth_with_clusters.json"
generate_and_store_multiple_data_sets(simulate_tumor_growth_with_clusters, file_simulate_tumor_growth_with_clusters,
                                      num_sets)
