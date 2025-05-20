#db = Database()
#data = db.execute_file('sql_scripts/select/oznamy.sql')

def interpretate_oznamy(data):
    tyzden = {}
    for row in data:
        date_id = row[0]
        datum = row[1]
        datum_popis = row[2]
        if date_id not in tyzden:
            tyzden[date_id] = [datum, datum_popis, []]
        tyzden[date_id][2].append(row[3:])

    return tyzden