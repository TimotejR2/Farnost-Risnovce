import sqlite3
import os

from .other import read_file
""" How to use example
db = Database("my_database.db")
schema = "CREATE TABLE example (id INTEGER PRIMARY KEY, name TEXT);"
db.create(schema)

db.execute("INSERT INTO example (name) VALUES ('John');")

data = db.read_table("example")
print(data)

schema = db.schema()
print(schema)
db.delete()
"""


class Database:
    def __init__(self, db_name, tmp=True):
        if db_name is None:
            raise ValueError('No database name provided')
        
        if tmp:
            self.db_path = os.path.join("/tmp", db_name)
        else:
            self.db_path = db_name

    def create(self, config_path):
        if os.path.exists(self.db_path):
            print('Database exists')
            return 'Database exists'

        # Get schema from config file
        schema = read_file(config_path)

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.executescript(schema)
        conn.commit()
        conn.close()

    def read_table(self, table, limit='NULL'):
        if os.path.exists(self.db_path):
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM {table} LIMIT {limit};")
            results = cursor.fetchall()
            conn.close()
            return results

        raise FileNotFoundError('Database not found')

    def execute(self, sql_command, *args):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(sql_command, args)
        conn.commit()
        conn.close()
        return True

    def schema(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT sql FROM sqlite_master WHERE type='table';")
        schema = cursor.fetchall()
        conn.close()
        return schema

    def delete(self):
        try:
            os.remove(self.db_path)
        except (FileNotFoundError, OSError):
            raise ValueError('File could not be removed')

