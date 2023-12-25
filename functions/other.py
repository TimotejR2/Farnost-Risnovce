from flask import make_response
import ast

def get_html(path, dynamic_values={}):
    with open(path, 'r') as file:
        html = file.read()
    for key, value in dynamic_values.items():
        key = '{{'+key+'}}'
        html = html.replace (key, value)
    return html

def error(code):
    
    from .security import get_data
    if code == 404 or code == 422:
        if code == 404:
            respond = (make_response(get_html('static/404.html'), code))
        else:
            respond = (make_response('Požiadavka nemohla byť spracovaná. Obsahuje neplatné alebo chýbajúce informácie, ktoré server nedokázal spracovať.', code))
    else:
        respond = []
        respond.append(get_data(code))
        if code == 403:
            respond.append ( make_response('Prístup odmietnutý.', code))
        elif code == 401:
            respond.append  (make_response('Skontrolujte heslo.', code))
        elif code == 400:
            respond.append  (make_response('Error 400. Ak sú údaje správne zadané, kontaktujte správcu emailom na timotej.ruzicka@gmail.com', code))

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

