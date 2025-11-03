from config.config import EVENTS_IN_DAY_LIMIT
from flask import request

def add_oznamy():
    add = Add()
    tyzden_nadpis = request.form['tyzden_nadpis']
    
    tyzden_popis = request.form['tyzden_popis']

    tyzden_zaciatok = request.form['tyzden_zaciatok']

    tyzden_id = add.tyzden(tyzden_nadpis, tyzden_popis, tyzden_zaciatok)
    
    for i in range(7):
        datum = request.form[('datum'+str(i))]

        if datum != "":
            den_nadpis = request.form[('den_nadpis'+str(i))]

            add.day(datum, den_nadpis, tyzden_id)
            

            for j in range(EVENTS_IN_DAY_LIMIT):

                udalost_popis = request.form['blok'+str(i)+'-udalost_popis-'+str(j)]
                udalost_miesto = request.form['blok'+str(i)+'-udalost_miesto-'+str(j)]
                udalost_cas = request.form['blok'+str(i)+'-cas'+str(j)]
                if not udalost_popis or not udalost_miesto or not udalost_cas:
                    break
                else:

                    add.udalost(udalost_popis, udalost_miesto, udalost_cas, add.last_date_id + 1 + i)

        else:
            break
    if add.day_args_list:
        add.cur.executemany(add.day_sql_query, add.day_args_list)
    if add.udalost_args_list:
        add.cur.executemany(add.udalost_sql_query, add.udalost_args_list)

    add.con.commit()
    add.cur.close()
    add.con.close()
    return

class Add:
    sql_comand = None
    def __init__(self):
        from ..database.database import Database
        self.db = Database()
        self.con = self.db.get_conn()
        self.cur = self.con.cursor()
        val = self.db.execute('SELECT id FROM oznamy_datum ORDER BY id DESC LIMIT 1;')
        self.last_date_id = int(val[0][0]) if val else None

        self.udalost_sql_query = 'INSERT INTO oznamy_udalost (datum_id, cas, miesto, popis) VALUES (%s, %s, %s, %s);'
        self.udalost_args_list = []

        self.day_sql_query = 'INSERT INTO oznamy_datum (datum, nazov, tyzden_id) VALUES (%s, %s, %s) RETURNING id;'
        self.day_args_list = []

    def tyzden(self, nadpis, popis, zaciatok):
        val = self.db.execute(
            'INSERT INTO oznamy_tyzden (tyzden_zaciatok, nadpis, popis) VALUES (%s, %s, %s) RETURNING id;',
            (zaciatok, nadpis, popis)
        )
        return int(val[0][0])

    def day(self, datum, nazov, tyzden_id):
        self.day_args_list.append((datum, nazov, tyzden_id))

    def udalost(self, popis, miesto, cas, datum_id):
        self.udalost_args_list.append((datum_id, cas, miesto, popis))

