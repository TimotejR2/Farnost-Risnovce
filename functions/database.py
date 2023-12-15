import sqlite3
def read():
    con = sqlite3.connect("data.db")
    db = con.cursor()
    db.execute("SELECT * FROM novinky;")
    results = db.fetchall()
    return results

def insert(nazov, image, alt, date, text):
    list =  (123, nazov, image, alt, date, text)
    return list