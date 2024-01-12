from flask import request

def get_data(code):
    """
    Gathers request-related data.

    Args:
    - code (int): HTTP status code.

    Returns:
    - dict: Request-related data including User Agent, IP Address, Request Method, URL Visited, and Code.
    """
    data = {
        "User Agent": request.headers.get('User-Agent'),
        "IP Address": request.remote_addr,
        "Request Method": request.method,
        "URL Visited": request.url,
        "Code": code
    }
    return data