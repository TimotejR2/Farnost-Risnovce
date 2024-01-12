from ..database import Database
from . import hash_password

db = Database()
def login(password, user='farar'):
    """
    Validates login credentials for a specific user.

    Args:
    - password (str): Password to be verified.
    - user (str): Username (default: 'farar').

    Returns:
    - bool: True if login is successful, False otherwise.
    """
    hashed_password = hash_password.hash_password(password)
    hash = db.execute_file('sql_scripts/get_hash.sql', (user, ))[0][0]
    return hash == hashed_password