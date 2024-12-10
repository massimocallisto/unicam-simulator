import re
import numbers


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
    alist = list(output_keys)
    alist.sort()
    return alist  # Convert the set back to a list


def get_variable_value(var_name, local_scope=None, additional_map=None):
    """
    Retrieve the value of a variable given its name as a string.

    Args:
        var_name (str): The name of the variable to retrieve.
        local_scope (dict, optional): A dictionary of local variables (e.g., locals()).
        additional_map (dict, optional): A dictionary of additional variables (e.g., class object variables()).

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

    # Check in the global scope
    if additional_map and var_name in additional_map:
        return additional_map[var_name]

    # Raise an error if the variable does not exist
    #raise NameError(f"Variable '{var_name}' is not defined in either the local or global scope.")
    return None


def replace_placeholder(data, placeholder, value):
    if isinstance(data, dict):
        for k, v in data.items():
            if isinstance(v, str) and v in placeholder:
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

#
# def replace_variables(input_string, replacements):
#     """
#     Replaces all occurrences of variables in the format ${var} with corresponding values from the replacements dictionary.
#
#     Args:
#         input_string (str): The string containing placeholders.
#         replacements (dict): A dictionary mapping variable names to their replacement values.
#
#     Returns:
#         str: The string with placeholders replaced.
#     """
#     # Regex to match ${...}
#     pattern = re.compile(r"\${(.*?)}")
#
#     def replacer(match):
#         # Extract variable name from the match
#         var_name = match.group(1)
#         # Replace with the corresponding value, or leave unchanged if not found
#         return str(replacements.get(var_name, match.group(0)))
#
#     # Substitute using the replacer function
#     return pattern.sub(replacer, input_string)