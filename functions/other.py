from flask import make_response
import ast

def get_html(path):
    with open(path, 'r') as file:
        html = file.read()
    return html

def error(code):
    if code == 404:
        return make_response(get_html('static/404.html'), 404)
    if code == 403:
        return make_response('Prístup odmietnutý, skontrolujte zadané heslo.', 403)





def strtolist(input_string):
    # Remove brackets at start and end, split by '],[' to get individual list strings
    list_strings = input_string.strip('[ ]').split('],[')
    lists = []
    for row_str in list_strings:
        row = ast.literal_eval('[' + row_str + ']')
        row = [str(elem).strip(" '") for elem in row]
        lists.append(row)
    return lists


