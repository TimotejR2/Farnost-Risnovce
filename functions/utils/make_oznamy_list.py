from config.config import EVENTS_IN_DAY_LIMIT

def make_oznamy_list():
    oznamy_list = []
    days_submited = days_submited_count()

    oznamy_list.append(request.form['datum'])
    for i in range (days_submited):
        var = [] # All events in day
        for j in range (EVENTS_IN_DAY_LIMIT):
            if request.form['blok'+str(i)+'-cas'+str(j)] == "":
                break
            
            text1 = request.form['blok'+str(i)+'-text'+str(j)+'-1']
            text2 = request.form['blok'+str(i)+'-text'+str(j)+'-2']
            time = request.form['blok'+str(i)+'-cas'+str(j)]
            var.append([text1, time, text2])

        var.append(convert_date(request.form['datum'+str(i)]))
        oznamy_list.append(var)
    oznamy_list.append(request.form['notes'])
    return oznamy_list

def days_submited_count():
    for i in range (7):
        if request.form[('datum'+str(i))] == "":
            if i == 0:
                return error(422)
            days_submited = i
            return days_submited
    raise ValueError('No data submited')
