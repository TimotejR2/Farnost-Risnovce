from ..database import Database
db = Database()

from argon2 import PasswordHasher

def login(password: str, user: str) -> bool:
    """
    Validates login credentials for a specific user.

    Args:
    - password (str): Password to be verified.
    - user (str): Username.

    Returns:
    - bool: True if login is successful, False otherwise.
    """
    # 1. Načítaj uložený hash z DB pre daného používateľa
    result = db.execute_file('sql_scripts/security/get_user_hash.sql', (user,))
    
    if not result:
        return False  # používateľ neexistuje
    
    stored_hash = result[0][0]

    # 2. Over heslo proti uloženému hashu
    ph = PasswordHasher()
    try:
        ph.verify(stored_hash, password)
        return True
    except:
        return False
