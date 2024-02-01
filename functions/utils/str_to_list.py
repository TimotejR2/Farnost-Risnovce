from ast import literal_eval

def str_to_list(string):
    """
    Convert a string representation of a list to an actual list.

    Parameters:
    string (str): String representation of a list.

    Returns:
    list: The converted list.
    """
    result_list = []

    for data_tuple in string:
        # Extract the string from the tuple
        string_representation = data_tuple[0]

        # Convert the string representation to a list
        converted_list = literal_eval(string_representation)

        # Append the converted list to the result list
        result_list.append(converted_list)

    return result_list
