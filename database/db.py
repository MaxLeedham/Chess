import sqlite3

conn = sqlite3.connect("database/game_database.db")
cursor = conn.cursor()


def commit():
    conn.commit()


def with_commit(func):
    def inner(*args, **kwargs):
        func(*args, **kwargs)
        commit()

    return inner


def close():
    conn.close()


def select(query: str, *values):
    cursor.execute(query, tuple(*values))
    return cursor.fetchall()


@with_commit
def execute(query: str, *values) -> int:
    cursor.execute(query, tuple(*values))
    return cursor.rowcount
