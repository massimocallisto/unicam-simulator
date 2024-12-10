import json
import numbers
import time
import random
from datetime import datetime, timedelta
import pytz
import re


def run(ref, config):
    # Parse the input JSON configuration
    params = config['params']
    data_model = config['data_model']

    # Extract parameters
    tz = pytz.timezone(params['TZ'])
    interval = params['T']
    min_temp = params['MIN']
    max_temp = params['MAX']
    output_keys = collect_output_keys(data_model)#params['output_keys']

    # Initialize the start time
    current_time = datetime.now(tz)

    try:
        while True:
            # Generate a random temperature
            temperature = random.uniform(min_temp, max_temp)

            # Create a copy of the data_model to modify
            output = json.loads(json.dumps(data_model))

            # Replace placeholders in the data_model
            for key in output_keys:
                current_value = get_variable_value(key, locals())
                if current_value is None:
                    continue
                output = replace_placeholder(output, f"${{{key}}}", current_value)

            # Print the output JSON
            print(json.dumps(output))

            # Wait for the specified interval
            time.sleep(interval)
    except KeyboardInterrupt:
        print("Simulation stopped.")


def collect_output_keys(data_model):
    """
    Recursively traverse the data_model and collect all values that start with "${" and end with "}".
    Handles multiple placeholders in the same string.

    Args:
        data_model (dict or list): The data_model to search.

    Returns:
        list: A list of unique output keys extracted from the data_model.
    """
    output_keys = set()  # Use a set to avoid duplicates

    def traverse(data):
        if isinstance(data, dict):
            for value in data.values():
                traverse(value)
        elif isinstance(data, list):
            for item in data:
                traverse(item)
        elif isinstance(data, str):
            # Find all "${...}" patterns in the string
            matches = re.findall(r"\${(.*?)}", data)
            output_keys.update(matches)

    traverse(data_model)
    return list(output_keys)  # Convert the set back to a list

def get_variable_value(var_name, local_scope=None):
    """
    Retrieve the value of a variable given its name as a string.

    Args:
        var_name (str): The name of the variable to retrieve.
        local_scope (dict, optional): A dictionary of local variables (e.g., locals()).

    Returns:
        Any: The value of the variable if found.

    Raises:
        NameError: If the variable does not exist in either scope.
    """
    # Check in the local scope first, if provided
    if local_scope and var_name in local_scope:
        return local_scope[var_name]

    # Check in the global scope
    if var_name in globals():
        return globals()[var_name]

    # Raise an error if the variable does not exist
    #raise NameError(f"Variable '{var_name}' is not defined in either the local or global scope.")
    return None


def replace_placeholder(data, placeholder, value):
    if isinstance(data, dict):
        for k, v in data.items():
            if isinstance(v, str) and v == placeholder:
                if isinstance(value, numbers.Number):
                    data[k] = value
                else:
                    data[k] = str(value)
        return data
    elif isinstance(data, list):
        for index, item in enumerate(data):
            if not isinstance(item, str):
                data[index] = replace_placeholder(item, placeholder, value)
            elif item == placeholder:
                if isinstance(value, numbers.Number):
                    data[index] = value
                else:
                    data[index] = str(value)
        return data
    else:
        return data


if __name__ == "__main__":
    # Example configuration
    ref = "jzp://edv.0001"

    config = {
        "params": {
            "TZ": "UTC",
            "T": 5,
            "MIN": -10,
            "MAX": 40
        },
        "data_model": {
            "ref": "${ref}",
            "tz": "${current_time}",
            "temperature": "${temperature}",
            "unit" : "°"
        }
    }
    run(ref, config)
