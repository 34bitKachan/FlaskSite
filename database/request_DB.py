import sqlite3


def add_article(title: str, text: str):
    with sqlite3.connect('article.db') as db:
        db.execute('INSERT INTO par (title, text) VALUES (?, ?)', (title, text))
        db.commit()


def get_articles():
    with sqlite3.connect('article.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM par')
        columns = [column[0] for column in cursor.description]  # Получаем названия колонок
        articles = cursor.fetchall()
        return [dict(zip(columns, article)) for article in articles]
