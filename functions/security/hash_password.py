from argon2 import PasswordHasher

def hash_password(password: str) -> str:
    """
    Hashes the provided password using Argon2 (a secure password hashing algorithm).

    Args:
    - password (str): Password to be hashed.

    Returns:
    - str: Hashed password using Argon2.
    """
    ph = PasswordHasher()
    hashed = ph.hash(password)
    return hashed