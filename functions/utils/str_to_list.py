from ast import literal_eval

from ..security import get_data

def strtolist(input_string):
    """
    Converts a string representation of nested lists to a list of lists.

    Args:
    - input_string (str): String representation of nested lists.

    Returns:
    - list of lists: Converted nested lists.
    """
    list_strings = input_string.strip('[ ]').split('],[')
    lists = []
    for row_str in list_strings:
        row = literal_eval('[' + row_str + ']')
        row = [str(elem).strip(" '") for elem in row]
        lists.append(row)
    return lists