from ..database import Database
from . import hash_password

db = Database()

def login(password: str, user: str) -> bool:
    """
    Validates login credentials for a specific user.

    Args:
    - password (str): Password to be verified.
    - user (str): Username.

    Returns:
    - bool: True if login is successful, False otherwise.
    """
    hashed_password = hash_password.hash_password(password)
    login_successful = bool(db.execute_file('sql_scripts/security/compare_hash.sql', (user, hashed_password)))
    return login_successful