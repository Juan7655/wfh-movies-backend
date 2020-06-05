import os

import psycopg2 as psycopg2
from psycopg2.extensions import parse_dsn
from contextlib import contextmanager

db_url = os.getenv('DATABASE')
db_params = parse_dsn(db_url)


@contextmanager
def open_cursor():
    conn = None
    try:
        conn = psycopg2.connect(**db_params)
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