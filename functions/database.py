import sqlite3
import os

from .other import read_file

class Database:
    def __init__(self, db_name):
        if db_name is None:
            raise ValueError('No database name provided')
        self.db_path = db_name

    def create(self, config_path):
        # Get schema from config file
        schema = read_file(config_path)

        # If database exist, check if it has actual schema
        if os.path.exists(self.db_path):
            existing_schema = self.schema()
            if existing_schema == schema:
                return 'Database is same'
            else:
                print('Old database was removed because of being outdate')
                self.delete()

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
        schema = schema[0][0]
        schema = schema + ';'
        conn.close()
        return schema

    def delete(self):
        os.remove(self.db_path)