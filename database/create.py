import sqlite3


def initDB():
    with sqlite3.connect("article.db") as db:
        db.execute("""CREATE TABLE IF NOT EXISTS par (
                    id INTEGER PRIMARY KEY,
                    title VARCHAR(255) NOT NULL,
                    text TEXT NOT NULL
                    )""")

        db.execute("""CREATE TABLE IF NOT EXISTS users (
                            id INTEGER PRIMARY KEY,
                            username VARCHAR(255) NOT NULL,
                            password VARCHAR(255) NOT NULL,
                            email VARCHAR(255) NOT NULL
                            )""")

        db.commit()
