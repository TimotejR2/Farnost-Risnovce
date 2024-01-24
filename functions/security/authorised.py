from typing import Union, Tuple

from ..database import Database
from flask import request
from datetime import datetime

db = Database()

def authorised(level: int) -> bool:
    """
    Checks if the user is authorized based on session, user level, and IP address.

    Args:
    - level (int): Minimum authorization level required.

    Returns:
    - bool: True if authorized, False otherwise.
    """
    # If session is invalid or not submitted
    id_and_ip = session_valid()
    if id_and_ip is False:
        return False

    # If user level is too high (lower permissions)
    id = id_and_ip[0]
    user_level = db.execute('SELECT level FROM users WHERE user_id = %s', (id, ))[0][0]
    if user_level > level:
        return False
    
    # Verify IP
    ip = id_and_ip[1]
    if ip != request.remote_addr:
        return False

    return True

def session_valid() -> Union[Tuple[int, str], bool]:
    """
    Checks the validity of the user session.

    Returns:
    - Union[Tuple[int, str], bool]: Tuple containing user ID and IP address if the session is valid, 
      or False if the session is invalid.
    """
    # Returns the name of the user that is logged in
    session = request.cookies.get("session")
    if not session:
        return False
    id_and_ip = db.execute_file('sql_scripts/security/get_id_and_ip_from_session.sql', (session, datetime.now()))
    if not id_and_ip:
        return False
    return id_and_ip[0]