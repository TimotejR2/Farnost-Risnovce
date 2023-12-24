import hashlib
def hash(password):
    hashed = hashlib.sha3_256(password.encode()).hexdigest()
    return hashed

def login(password, user='farar'):
    if user == 'farar':
        if hash(password) == 'a00e4d3b352e9d11979549b9eef5dc951592f594488451e6cd86fdc4bce76a53':
            return True
    if user == 'root':
        if hash(password) == 'fb001dfcffd1c899f3297871406242f097aecf1a5342ccf3ebcd116146188e4b':
            return True
    return False

def get_data(code):
    from flask import request

    data = {
        "User Agent": request.headers.get('User-Agent'),
        "IP Address": request.remote_addr,
        "Request Method": request.method,
        "URL Visited": request.url,
        "Code": code
    }
    return data

def login_required(f):
    from functools import wraps
    from flask import session, redirect
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def root_required(f):
    from functools import wraps
    from flask import session, redirect
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") != 'root':
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function