from functools import wraps
from datetime import timedelta, datetime
from config.config import DELAY_BETWEEN_WRONG_LOGINS

def security_delay(f):
    from .. import error
    from . import Database
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check if there were not too many login attempts in the past
        delay = timedelta(days=DELAY_BETWEEN_WRONG_LOGINS)
        now = datetime.now()
        wrong = Database().execute_file('sql_scripts/security/get_wrong_count.sql', (now - delay,))[0][0]

        if wrong > 2:
            return error(429)
        return f(*args, **kwargs)
    return decorated_function