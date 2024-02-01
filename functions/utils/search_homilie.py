from flask import request, render_template
from datetime import datetime, timedelta
from config.config import HOMILIE_SEARCH_DAYS
from .error import error
from ..database.database import Database  # Import Database class locally

def search_homilie():
    """
    Search for homilies within a specified date range and render the results.

    Returns:
    render_template: HTML template with homily search results.

    Raises:
    error(422): If no date is provided in the form.
    error(404): If no homilies are found within the specified date range.
    """
    db = Database()

    # Get the date from the form
    datum = request.form['date']
    if datum == '':
        return error(422)

    # Convert the date and define search date range
    datum = datetime.strptime(datum, '%Y-%m-%d')
    datum1 = datum + timedelta(days=HOMILIE_SEARCH_DAYS)
    datum2 = datum - timedelta(days=HOMILIE_SEARCH_DAYS)

    # Execute the SQL query
    result = db.execute('SELECT * FROM homilie WHERE datum < %s::timestamp AND datum > %s::timestamp', (str(datum1), str(datum2)))

    # Return error if no homilies found, else render the template
    if len(result) == 0:
        return error(404)
    return render_template('homilie.html', list=result)
