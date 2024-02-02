import secrets
from flask import request
from ..database import Database
from datetime import datetime, timedelta
from config.config import SESSION_AGE_LIMIT
db = Database()

def generate_session(username: str) -> str:
    """
    Generates a session for the given username and inserts it into the database.

    Args:
    - username (str): Username for which the session is generated.

    Returns:
    - str: The generated session token.
    """
    session = secrets.token_hex(16)
    valid = session_valid_date()
    ip_address = request.remote_addr
    
    db.execute_file('sql_scripts/security/insert_session.sql', (username, session, valid, ip_address))
    return session


def session_valid_date() -> datetime:
    """
    Generates a datetime object representing the validity date for a session.

    Returns:
    - datetime: The validity date for the session based on congig.
    """
    current_date = datetime.now()
    valid_date = current_date + timedelta(seconds=SESSION_AGE_LIMIT)
    return valid_date
