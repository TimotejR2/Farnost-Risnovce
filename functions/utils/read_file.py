def read_file(path=None):
    """
    Read the contents of a file.

    Parameters:
    path (str): Path to the file.

    Returns:
    str: Contents of the file.

    Raises:
    ValueError: If no path is provided.
    """
    if path is None:
        raise ValueError('No path provided to read_file function')
    
    file = open(path, "r")
    return file.read()
