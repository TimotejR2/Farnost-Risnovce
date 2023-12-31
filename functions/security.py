import hashlib
import random
from flask import request

from .csv import csv_values, csv_keys, read_csv

def hash_password(password):
    """
    Hashes the provided password using SHA3-256 encryption.

    Args:
    - password (str): Password to be hashed.

    Returns:
    - str: Hashed password.
    """
    hashed = hashlib.sha3_256(password.encode()).hexdigest()
    return hashed

def login(password, user='farar'):
    """
    Validates login credentials for a specific user.

    Args:
    - password (str): Password to be verified.
    - user (str): Username (default: 'farar').

    Returns:
    - bool: True if login is successful, False otherwise.
    """
    hashed_passwords = {
        'farar': 'a00e4d3b352e9d11979549b9eef5dc951592f594488451e6cd86fdc4bce76a53',
        'root': 'fb001dfcffd1c899f3297871406242f097aecf1a5342ccf3ebcd116146188e4b'
    }

    if user in hashed_passwords:
        return hash_password(password) == hashed_passwords[user]
    
    return False

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

def generate_session(possible_sessions=None, user=None):
    """
    Generates a session string.

    Args:
    - possible_sessions (list): List of possible session strings.
    - user (str): User identification (e.g., username).

    Returns:
    - str: Randomly selected session string from the given list.
    
    Raises:
    - ValueError: If not all parameters were submitted to generate_session function.
    """
    if user is None or possible_sessions is None:
        raise ValueError('Not all parameters were submitted to generate_session function')

    random_session = random.choice(possible_sessions)
    return random_session

def get_session_from_csv(user):
    """
    Retrieves a session string from a CSV file based on the user.

    Args:
    - user (str): User identification (e.g., username).

    Returns:
    - str: Session string retrieved from the CSV file.

    Uses functions from the 'csv' module to process CSV data.
    """
    sessions_data = read_csv('static/data/sessions.csv')
    filtered_sessions = csv_keys(data=sessions_data, key=user)
    possible_sessions = csv_values(data=filtered_sessions)
    session = generate_session(possible_sessions=possible_sessions, user=user)
    return session

def user_logged_in(user=None, sessions_path="static/data/sessions.csv"):
    """
    Checks if a user is logged in based on session cookies.

    Args:
    - user (str, optional): The username to check. If None, checks for any logged-in user.
    - sessions_path (str): Path to the sessions CSV file.

    Returns:
    - bool: True if the user is logged in, False otherwise.
    """
    # Read the CSV file
    data = read_csv(sessions_path)

    # Check if session cookie exists
    if request.cookies.get('session') is None:
        return False

    # If user is not specified, get all sessions
    if user is None:
        correct_sessions = csv_values(data=data)
    else:
        # Retrieve sessions for the specified user
        user_sessions_raw = csv_keys(data=data, key=user)
        correct_sessions = csv_values(user_sessions_raw)

    # Check if the session cookie matches any valid session
    if request.cookies.get("session") not in correct_sessions:
        return False

    return True
