import os
import psycopg2
from decouple import config


class Connection:
    def __init__(self) -> None:
        if os.uname()[1] == "LAPTOP-1O7S9IJH":
            self.host, self.dbname, self.user, self.password = config("PGHOST"),config("PGDBNAME"),config("PGUSER"),config("PGPASSWORD")
    
    def __enter__(self):
        if os.uname()[1] == "LAPTOP-1O7S9IJH":
            self.conn = psycopg2.connect(f"host={self.host} dbname={self.dbname} user={self.user} password={self.password}")
        else:
            self.conn = psycopg2.connect(os.getenv("DATABASE_URL"))

        self.conn.set_session(autocommit=True)

        return self.conn
    
    def __exit__(self, type, value, traceback):
        self.conn.close()

