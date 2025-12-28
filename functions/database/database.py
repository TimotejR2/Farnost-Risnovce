import psycopg2
import os
from ..utils import read_file

POSTGRES = os.environ.get("POSTGRES_URL")
if not POSTGRES:
    POSTGRES = read_file('config/postgres.sql')
    if not POSTGRES:
        raise ValueError("POSTGRES_URL environment variable not set")

SCHEMA_PATH = 'config/schema.sql'

class Database:
    """
    Database class for interacting with PostgreSQL database.

    Attributes:
    POSTGRES (str): PostgreSQL connection string.
    SCHEMA_PATH (str): Path to the SQL schema file.

    Methods:
    - create(): Create database schema.
    - read_table(table_name, limit=None, id=None): Read data from a table with optional limit and ID filter.
    - execute_file(path, args=None): Execute SQL queries from a file.
    - execute(sql_query, args=None): Execute a SQL query with optional parameters.
    """
    def create(self):
        """Create database schema."""
        self.execute_file(SCHEMA_PATH)

    def read_table(self, table_name, limit=None, id=None):
        """
        Read data from a table with optional limit and ID filter.

        Parameters:
        - table_name (str): Name of the table to read.
        - limit (int): Maximum number of rows to retrieve.
        - id (int): Optional ID filter for the query.

        Returns:
        list: List of results from the query.
        """
        if id is None:
            id = ' <> -1'
        else:
            id = '= ' + str(id)
        sql_raw = read_file('sql_scripts/select/select.sql')
        sql_query = sql_raw.format(table_name=table_name, id=id)
         
        output = self.execute(sql_query, (limit, ))
        if not output:
            return []
        if len(output) <= 1:
            output = output[0]
        if not output:
            output = []
        return output

    def execute_file(self, path, args=None):
        """
        Execute SQL queries from a file.

        Parameters:
        - path (str): Path to the SQL file.
        - args (tuple): Optional parameters for the query.

        Returns:
        Any: Results of the query.
        """
        sql_query = read_file(path)
        return self.execute(sql_query, args)

    def execute(self, sql_query, args=None, fetchone=False):
        try:
            with psycopg2.connect(POSTGRES) as conn:
                with conn.cursor() as cur:
                    cur.execute(sql_query, args)

                    if fetchone:
                        return cur.fetchone()
                    return cur.fetchall()

        except psycopg2.Error as e:
            print(f"DB error: {e}")
            return None


    def get_conn(self):
        conn = psycopg2.connect(POSTGRES)
        return conn
