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