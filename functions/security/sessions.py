import secrets
from flask import request
from ..database import Database
db = Database()

def generate_session(username):
    session = secrets.token_hex(16)
    valid = session_valid_date()
    ip_address = request.remote_addr
    db.execute_file('sql_scripts/security/insert_session.sql', (username, session, valid, ip_address))
    return session

from datetime import datetime, timedelta
def session_valid_date():
    current_date = datetime.now()
    valid_date = current_date + timedelta(days=100)
    return valid_date