import csv

def csv_keys(data=None, key=None):
    """
    Filters CSV data based on a specified key.

    Args:
    - data (list of dict): List of dictionaries representing CSV rows.
    - key (str): Key to filter the CSV data.

    Returns:
    - list of dict: Filtered rows based on the specified key.
    
    Raises:
    - ValueError: If data or key parameters are missing.
    """
    if data is None or key is None:
        raise ValueError('Not all parameters were submitted to csv_keys function')
    
    final_rows = []
    for row in data:
        if row['key'] == key:
            final_rows.append(row)

    return final_rows

def csv_values(data=None):
    """
    Extracts values from CSV data.

    Args:
    - data (list of dict): List of dictionaries representing CSV rows.

    Returns:
    - list: Extracted values from the CSV data.
    
    Raises:
    - ValueError: If data parameter is missing.
    """
    if data is None:
        raise ValueError('Not all parameters were submitted to csv_values function')
    
    values = []
    for row in data:
        values.append(row['value'])

    return values

def read_csv(csv_path=None):
    """
    Reads a CSV file and returns its content as a list of dictionaries.

    Args:
    - csv_path (str): Path to the CSV file.

    Returns:
    - list of dict: Content of the CSV file represented as a list of dictionaries.
    
    Raises:
    - ValueError: If csv_path parameter is missing.
    """
    if csv_path is None:
        raise ValueError('Not all parameters were submitted to read_csv function')

    values = []
    with open(csv_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            values.append(row)
    return values
