import sqlite3

def read(db_path="data.db"):
    """
    Reads all records from the 'novinky' table in the specified SQLite database.

    Args:
    - db_path (str): Path to the SQLite database file (default: 'data.db').

    Returns:
    - list of tuples: List of tuples representing the fetched records.
    """
    con = sqlite3.connect(db_path)
    db = con.cursor()
    db.execute("SELECT * FROM novinky;")
    results = db.fetchall()
    con.close()
    return results

def insert(nazov, image, alt, date, text, id):
    """
    Creates a list with provided data.

    Args:
    - nazov (str): Title.
    - image (str): Image URL.
    - alt (str): Alternate text for the image.
    - date (str): Date of the news.
    - text (str): Content text of the news.
    - id (int): ID number of new post.

    Returns:
    - list: List containing provided data in a specific order.
    """
    data_list = (id, nazov, image, alt, date, text)
    return data_list
