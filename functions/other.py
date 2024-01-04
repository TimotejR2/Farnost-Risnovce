from flask import make_response
from .security import get_data
import ast

def get_html(path, dynamic_values={}):
    """
    Reads an HTML file and substitutes placeholders with dynamic values.

    Args:
    - path (str): Path to the HTML file.
    - dynamic_values (dict): Dictionary containing dynamic key-value pairs to replace in the HTML.

    Returns:
    - str: HTML content with replaced dynamic values.
    """
    with open(path, 'r') as file:
        html = file.read()

    for key, value in dynamic_values.items():
        placeholder = '{{' + key + '}}'
        html = html.replace(placeholder, value)

    return html

def error(code):
    """
    Generates error responses based on the provided HTTP status code.

    Args:
    - code (int): HTTP status code.

    Returns:
    - make_response or list: Response(s) corresponding to the given HTTP status code.
    """
    if code == 404:
        return make_response(get_html('static/404.html'), code)
    elif code == 422:
        return make_response('Požiadavka nemohla byť spracovaná. Obsahuje neplatné alebo chýbajúce informácie, ktoré server nedokázal spracovať.', code)
    elif code in [400, 401, 403]:
        responses = [get_data(code)]

        error_messages = {
            400: 'Error 400. Ak sú údaje správne zadané, kontaktujte správcu emailom na timotej.ruzicka@gmail.com',
            401: 'Skontrolujte heslo.',
            403: 'Prístup odmietnutý.'
        }

        responses.append(make_response(error_messages[code], code))
        return responses

    return []

def strtolist(input_string):
    """
    Converts a string representation of nested lists to a list of lists.

    Args:
    - input_string (str): String representation of nested lists.

    Returns:
    - list of lists: Converted nested lists.
    """
    list_strings = input_string.strip('[ ]').split('],[')
    lists = []
    for row_str in list_strings:
        row = ast.literal_eval('[' + row_str + ']')
        row = [str(elem).strip(" '") for elem in row]
        lists.append(row)
    return lists

def read_file(path=None):
    if path is None:
        raise ValueError('No path provided to read_file function')
    
    file = open(path, "r")
    return file.read()