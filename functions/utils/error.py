from flask import make_response
from . import get_html

def error(code):
    """
    Generates error responses based on the provided HTTP status code.

    Args:
    - code (int): HTTP status code.

    Returns:
    - make_response or list: Response(s) corresponding to the given HTTP status code.
    """

    error_messages = {
        400: 'Chybná žiadosť.',
        401: 'Neoprávnený prístup. Skontrolujte svoje heslo.',
        403: 'Zakázaný prístup. Prístup zamietnutý.',
        404: 'Stránka nenájdená.',
        422: 'Žiadosť nemohla byť spracovaná. Obsahuje neplatné alebo chýbajúce informácie, ktoré server nedokázal spracovať.',
        429: 'Príliš veľa pokusov o prihlásenie. Skúste to znovu neskôr.'
    }

    default_message = 'Došlo k chybe.'

    return make_response(get_html.get_html(f'static/{code}.html') if code == 404 else error_messages.get(code, default_message), code)
