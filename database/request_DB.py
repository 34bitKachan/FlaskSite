import sqlite3


def add_article(title: str, text: str):
    with sqlite3.connect('article.db') as db:
        db.execute('INSERT INTO par (title, text) VALUES (?, ?)', (title, text))
        db.commit()


def add_user(username: str, password: str, email: str) -> bool:
    result = False
    with sqlite3.connect('article.db') as db:
        cursor = db.cursor()
        cursor.execute("SELECT COUNT(*) FROM users WHERE username = ?", (username,))
        user_exists = cursor.fetchone()[0]
        print(user_exists)
        if user_exists == 0:
            cursor.execute("INSERT INTO users (username, password, email) VALUES (?, ?, ?)",
                           (username, password, email))
            db.commit()
            print("Пользователь добавлен в БД")
            result = True
    return result


def get_user_login(username: str, password: str) -> dict:
    with sqlite3.connect('article.db') as db:
        db.row_factory = sqlite3.Row
        cursor = db.cursor()
        user = cursor.execute("SELECT id, username, email FROM users WHERE username = ? AND password = ?",
                              (username, password)).fetchone()
    return user

def get_user_id(user_id) -> dict:
    with sqlite3.connect('article.db') as db:
        db.row_factory = sqlite3.Row
        cursor = db.cursor()
        user = cursor.execute("SELECT id, username, email FROM users WHERE username = ? AND password = ?",
                              (username, password)).fetchone()
    return user['id']


def get_articles():
    articles_dict = []
    with sqlite3.connect('article.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM par')
        columns = [column[0] for column in cursor.description]  # Получаем названия колонок
        articles = cursor.fetchall()
        articles_dict = [dict(zip(columns, article)) for article in articles]
    return articles_dict
