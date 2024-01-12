from ..database import Database
from flask import request
from datetime import datetime
db = Database()

def authorised(level):
    # If session is invalid or was not submited
    id_and_ip = session_valid()
    if id_and_ip is False:
        return False

    # If level of user is too big 
    # Big level means lower permissions
    id = id_and_ip[0]
    user_level = db.execute('SELECT level FROM users WHERE user_id = %s', (id, ))[0][0]
    if user_level > level:
        return False
    
    # Verify ip
    ip = id_and_ip[1]
    if ip != request.remote_addr:
        return False

    return True

def session_valid():
    # Returns name of user that is loged in
    session = request.cookies.get("session")
    if not session:
        return False
    id_and_ip = db.execute_file('sql_scripts/get_id_and_ip_from_session.sql', (session, datetime.now()))[0]
    if id_and_ip == []:
        return False
    return id_and_ip