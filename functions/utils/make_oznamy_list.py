from config.config import EVENTS_IN_DAY_LIMIT
from flask import request
from .convert_date import convert_date

def make_oznamy_list():
    """
    Create a list of announcements based on form data.

    Returns:
    oznamy_list (list): List containing date, events for each submitted day, and additional notes.
    """
    oznamy_list = []
    days_submitted = days_submitted_count()

    # Append date from the form
    oznamy_list.append(request.form['datum'])

    # Iterate over submitted days
    for i in range(days_submitted):
        var = []  # All events in a day

        # Iterate over events in a day
        for j in range(EVENTS_IN_DAY_LIMIT):
            if request.form['blok'+str(i)+'-cas'+str(j)] == "":
                break
            
            text1 = request.form['blok'+str(i)+'-text'+str(j)+'-1']
            text2 = request.form['blok'+str(i)+'-text'+str(j)+'-2']
            time = request.form['blok'+str(i)+'-cas'+str(j)]
            var.append([text1, time, text2])

        # Append the converted date for the day
        var.append(convert_date(request.form['datum'+str(i)]))
        oznamy_list.append(var)

    # Append additional notes from the form
    oznamy_list.append(request.form['notes'])
    return oznamy_list

def days_submitted_count():
    """
    Count the number of days for which data has been submitted through the form.

    Returns:
    days_submitted (int): Count of submitted days.
    
    Raises:
    ValueError: If no data is submitted for any day.
    """
    for i in range(7):
        if request.form[('datum'+str(i))] == "":
            if i == 0:
                return error(422)
            days_submitted = i
            return days_submitted
    raise ValueError('No data submitted')
