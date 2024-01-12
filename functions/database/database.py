import psycopg2
import os
from ..utils import read_file

POSTGRES = read_file('config/postgres.sql')
SCHEMA_PATH = 'config/schema.sql'

class Database:
    def create(self):
        self.execute_file(SCHEMA_PATH)

    def read_table(self, table_name, limit=None, id=None):
        if id == None:
            id = ' <> -1'
        else:
            id = '= '+ str(id)
        sql_raw = read_file('sql_scripts/select.sql')
        sql_query = sql_raw.format(table_name=table_name,id=id)
         
        output = self.execute(sql_query, (limit, ))
        if len(output) <= 1:
            output = output[0]
        if not output:
            output = []
        return output

    def execute_file(self, path, args=None):
        sql_query = read_file(path)
        return self.execute(sql_query, args)

    def execute(self, sql_query, args=None):
        conn = psycopg2.connect(POSTGRES)
        cur = conn.cursor()
        cur.execute(sql_query, args)
        try:
            output = cur.fetchall()
        except psycopg2.ProgrammingError:
            conn.commit()
            cur.close()
            conn.close()
            return 
            
        conn.commit()
        cur.close()
        conn.close()
        return output
