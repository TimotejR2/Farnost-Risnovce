def read_file(path=None):
    if path is None:
        raise ValueError('No path provided to read_file function')
    
    file = open(path, "r")
    return file.read()