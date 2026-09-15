import sqlite3
from datetime import datetime


DATABASE_NAME = "ranking.db"


def get_connection():

    connection = sqlite3.connect(
        DATABASE_NAME,
        check_same_thread=False
    )

    connection.row_factory = sqlite3.Row

    return connection


def create_table():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS scores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            score INTEGER NOT NULL,
            created_at TEXT NOT NULL
        )
        """
    )

    connection.commit()

    connection.close()


def save_score(name, score):

    if not name:
        name = "Player"

    name = name.strip()[:20]

    if score < 0:
        score = 0

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO scores
        (name, score, created_at)
        VALUES (?, ?, ?)
        """,
        (
            name,
            score,
            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        )
    )

    connection.commit()

    connection.close()


def get_ranking(limit=10):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            name,
            score,
            created_at
        FROM scores
        ORDER BY score DESC, id ASC
        LIMIT ?
        """,
        (limit,)
    )

    rows = cursor.fetchall()

    connection.close()

    return rows


create_table()
