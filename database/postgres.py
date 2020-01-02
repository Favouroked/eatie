import json
import os
from contextlib import contextmanager

import psycopg2
from psycopg2 import sql
from psycopg2.extras import RealDictCursor

DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_USERNAME = os.getenv('DB_USERNAME')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')


class Postgres:

    def __init__(self):
        self.host = DB_HOST
        self.port = DB_PORT
        self.username = DB_USERNAME
        self.password = DB_PASSWORD

    @contextmanager
    def get_connection(self, db):
        con = psycopg2.connect(
            host=self.host, port=self.port, database=db,
            user=self.username,
            password=self.password,
            cursor_factory=RealDictCursor
        )
        try:
            yield con
        finally:
            con.close()

    def create_database(self, db_name):
        with self.get_connection(DB_NAME) as conn:
            conn.set_isolation_level(0)
            cur = conn.cursor()
            cur.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(db_name)))
            conn.commit()
            cur.close()

    def insert_into_db(self, query, values, db=DB_NAME):
        with self.get_connection(db) as conn:
            try:
                cur = conn.cursor()
                cur.execute(query, values)
                conn.commit()
                cur.close()
                return True, None
            except (Exception, psycopg2.DatabaseError) as err:
                print("Database Error", err)
                raise Exception(err)

    def execute_query(self, query, params, db=DB_NAME):
        with self.get_connection(db) as conn:
            try:
                cur = conn.cursor()
                cur.execute(query, params)
                res = cur.fetchall()
                if res is not None:
                    return True, json.loads(json.dumps(res, default=str))
                else:
                    return True, []
            except (Exception, psycopg2.DatabaseError) as err:
                print('Database Error', err)
                raise Exception(err)
