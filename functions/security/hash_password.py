from hashlib import sha3_256

def hash_password(password: str) -> str:
    """
    Hashes the provided password using SHA3-256 encryption.

    Args:
    - password (str): Password to be hashed.

    Returns:
    - str: Hashed password using SHA3-256.
    """
    hashed = sha3_256(password.encode()).hexdigest()
    return hashed