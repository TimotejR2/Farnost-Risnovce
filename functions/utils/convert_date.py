from datetime import datetime

def convert_date(date):
    """
    Converts date from string in 'Y-M-D' format to 'D.M' format.

    Args:
    - date (str): Date to be changed in 'Y-M-D' format.

    Returns:
    - str: Converted date in 'D.M' format.
    """
    date = datetime.strptime(date, '%Y-%m-%d')
    new_date = date.strftime('%-d.%-m')
    return  new_date