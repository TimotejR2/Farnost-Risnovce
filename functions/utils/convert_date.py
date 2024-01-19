from datetime import datetime

def convert_date(date):
    d = datetime.strptime(date, '%Y-%m-%d')
    return d.strftime('%-d.%-m')