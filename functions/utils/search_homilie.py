from flask import request, render_template
from datetime import datetime, timedelta
from config.config import HOMILIE_SEARCH_DAYS
from .error import error

def search_homilie():
    from ..database.database import Database  # Import Database class locally
    db = Database()
    datum = request.form['date']
    if datum == '':
        return error(422)
    datum = datetime.strptime(datum, '%Y-%m-%d')
    datum1 = datum + timedelta(days=HOMILIE_SEARCH_DAYS)
    datum2 = datum - timedelta(days=HOMILIE_SEARCH_DAYS)
    result = db.execute('SELECT * FROM homilie WHERE datum < %s::timestamp AND datum > %s::timestamp', (str(datum1), str(datum2)))
    if len(result) == 0:
        return error(404)
    return render_template('homilie.html', list=result)
