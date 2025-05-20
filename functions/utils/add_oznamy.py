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

            datum_id = add.day(datum, den_nadpis, tyzden_id)
            

            for j in range(EVENTS_IN_DAY_LIMIT):

                udalost_popis = request.form['blok'+str(i)+'-udalost_popis-'+str(j)]
                udalost_miesto = request.form['blok'+str(i)+'-udalost_miesto-'+str(j)]
                udalost_cas = request.form['blok'+str(i)+'-cas'+str(j)]
                if not udalost_popis or not udalost_miesto or not udalost_cas:
                    break
                else:

                    add.udalost(udalost_popis, udalost_miesto, udalost_cas, datum_id)

        else:
            break
    add.con.commit()
    add.cur.close()
    add.con.close()
    return

class Add:
    def __init__(self):
        from ..database.database import Database
        self.db = Database()
        self.con = self.db.get_conn()
        self.cur = self.con.cursor()

    def tyzden(self, nadpis, popis, zaciatok):
        val = self.db.execute(
            'INSERT INTO oznamy_tyzden (tyzden_zaciatok, nadpis, popis) VALUES (%s, %s, %s) RETURNING id;',
            (zaciatok, nadpis, popis)
        )
        return int(val[0][0])

    def day(self, datum, nazov, tyzden_id):
        val = self.db.execute(
            'INSERT INTO oznamy_datum (tyzden_id, datum, nazov) VALUES (%s, %s, %s) RETURNING id;',
            (tyzden_id, datum, nazov)
        )
        return int(val[0][0])

    def udalost(self, popis, miesto, cas, datum_id):
        self.cur.execute(
            'INSERT INTO oznamy_udalost (datum_id, cas, miesto, popis) VALUES (%s, %s, %s, %s);',
            (datum_id, cas, miesto, popis)
        )

