from flask import make_response
from ..security import get_data
from . import get_html

def error(code):
    """
    Generates error responses based on the provided HTTP status code.

    Args:
    - code (int): HTTP status code.

    Returns:
    - make_response or list: Response(s) corresponding to the given HTTP status code.
    """
    if code == 404:
        return make_response(get_html.get_html('static/404.html'), code)
    elif code == 422:
        return make_response('Požiadavka nemohla byť spracovaná. Obsahuje neplatné alebo chýbajúce informácie, ktoré server nedokázal spracovať.', code)
    elif code in [400, 401, 403]:
        # TODO: Pridanie systemu na sledovanie neuspesnych pokusov

        error_messages = {
            400: 'Error 400. Ak sú údaje správne zadané, kontaktujte správcu emailom na timotej.ruzicka@gmail.com',
            401: 'Skontrolujte heslo.',
            403: 'Prístup odmietnutý.'
        }

        responses = (make_response(error_messages[code], code))
        return responses

    return []