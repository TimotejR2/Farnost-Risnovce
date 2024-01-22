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
    hash = db.execute_file('sql_scripts/security/get_hash.sql', (user, ))
    return bool(hash) and hash[0][0] == hashed_password
