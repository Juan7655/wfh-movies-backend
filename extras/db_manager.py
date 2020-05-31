from sqlalchemy import create_engine
import psycopg2 as psycopg2
from contextlib import contextmanager
import requests

host = "localhost"
database = "wfh-movies"
user = "postgres"
password = "admin123"


@contextmanager
def open_cursor():
    conn = None
    try:
        conn = psycopg2.connect(host=host, database=database, user=user, password=password)
        cur = conn.cursor()
        yield cur
        conn.commit()
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def decorator(fun):
    def wrapped(fetchall: bool = None, *args, **kwargs):
        result = None
        with open_cursor() as cur:
            cur.execute(fun(*args, **kwargs))
            if fetchall is not None:
                result = cur.fetchall() if fetchall else cur.fetchone()[0]
        return result

    return wrapped