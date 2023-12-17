from flask import make_response
import ast

def get_html(path):
    with open(path, 'r') as file:
        html = file.read()
    return html

def error(code):
    respond = []
    from .security import get_data
    respond.append(get_data(code))
    if code == 404:
        respond.append (make_response(get_html('static/404.html'), 404))
    elif code == 403:
        respond.append ( make_response('Prístup odmietnutý.', 403))
    elif code == 401:
        respond.append  (make_response('Skontrolujte heslo.', 401))
    elif code == 400:
        respond.append  (make_response('Error 400. Ak sú údaje správne zadané, kontaktujte správcu emailom na timotej.ruzicka@gmail.com', 400))
    return respond





def strtolist(input_string):
    # Remove brackets at start and end, split by '],[' to get individual list strings
    list_strings = input_string.strip('[ ]').split('],[')
    lists = []
    for row_str in list_strings:
        row = ast.literal_eval('[' + row_str + ']')
        row = [str(elem).strip(" '") for elem in row]
        lists.append(row)
    return lists


