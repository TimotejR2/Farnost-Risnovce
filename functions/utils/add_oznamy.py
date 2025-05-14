from config.config import EVENTS_IN_DAY_LIMIT
from flask import request
from datetime import datetime
from werkzeug.datastructures import ImmutableMultiDict

def add_oznamy():
    tyzden_nadpis = request.form['tyzden_nadpis']
    
    tyzden_popis = request.form['tyzden_popis']

    tyzden_zaciatok = request.form['tyzden_zaciatok']

    tyzden_id = add_tyzden(tyzden_nadpis, tyzden_popis, tyzden_zaciatok)
    
    for i in range(7):
        datum = request.form[('datum'+str(i))]

        if datum != "":
            den_nadpis = request.form[('den_nadpis'+str(i))]

            datum_id = add_day(datum, den_nadpis, tyzden_id)
            

            for j in range(EVENTS_IN_DAY_LIMIT):

                udalost_popis = request.form['blok'+str(i)+'-udalost_popis-'+str(j)]
                udalost_miesto = request.form['blok'+str(i)+'-udalost_miesto-'+str(j)]
                udalost_cas = request.form['blok'+str(i)+'-cas'+str(j)]
                if not udalost_popis or not udalost_miesto or not udalost_cas:
                    break
                else:

                    add_udalost(udalost_popis, udalost_miesto, udalost_cas, datum_id)

        else:
            break
    return

def add_tyzden(nadpis, popis, zaciatok):
    print('Add tyzden')
    from ..database.database import Database
    db = Database()
    db.execute_file('sql_scripts/user_insert/insert_tyzden.sql', (zaciatok, nadpis, popis))
    val = db.execute('SELECT id FROM oznamy_tyzden ORDER BY id DESC LIMIT 1')
    val = int(val[0][0])
    return val
    
def add_day(datum, nazov, tyzden_id):
    print(datum, nazov, tyzden_id)
    from ..database.database import Database
    db = Database()
    db.execute_file('sql_scripts/user_insert/insert_oznamy_datum.sql', (tyzden_id, datum, nazov))
    val = db.execute('SELECT id FROM oznamy_datum ORDER BY id DESC LIMIT 1')
    val = int(val[0][0])
    return val

def add_udalost(popis, miesto, cas, datum_id):
    print(popis, miesto, cas, datum_id)
    from ..database.database import Database
    db = Database()
    db.execute_file('sql_scripts/user_insert/insert_oznamy_udalost.sql', (datum_id, cas, miesto, popis))
    return
