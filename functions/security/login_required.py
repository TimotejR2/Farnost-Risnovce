from . import authorised
from flask import redirect
from functools import wraps

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not authorised(1):
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function