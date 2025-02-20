import sqlite3


def initDB():
    with sqlite3.connect("article.db") as db:
        db.execute("""CREATE TABLE IF NOT EXISTS par (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    title VARCHAR(255) NOT NULL,
                    text TEXT NOT NULL
                    )""")
        db.commit()
