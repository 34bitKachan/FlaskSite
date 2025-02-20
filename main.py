from flask import Flask, render_template, request, redirect, url_for
from database.create import initDB
from database.request_DB import add_article, get_articles, add_user, get_user_login

app = Flask(__name__)


@app.route("/")
def hello_world():
    return render_template('index.html')


@app.route("/about")
def about():
    return render_template('about.html')


@app.route("/reg", methods=["POST", "GET"])
def registration_user():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        if username != "" and email != "" and password != "":
            is_create = add_user(username=username, password=password, email=email)
            if is_create:
                return redirect('/')
            return render_template('registration/reg.html', mes="Имя пользователя занято")
        return render_template('registration/reg.html', mes="Заполните все поля!")
    return render_template('registration/reg.html')

@app.route("/sing_in", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username != "" and password != "":
            user = get_user_login(username=username, password=password)
            print(user)
            if user:
                return redirect('/')
            return render_template('registration/sing_in.html', mes="Неправильный логин или пароль")
        return render_template('registration/sing_in.html', mes="Заполните все поля!")
    return render_template('registration/sing_in.html')


@app.route("/article")
def get_article():
    print(get_articles())
    return render_template('article.html', posts=get_articles())


@app.route("/create", methods=["POST", "GET"])
def create_article():
    if request.method == "POST":
        title = request.form.get("title")
        text = request.form.get("text")
        print(title)
        print(text)
        add_article(title, text)
        return redirect("/")
    else:
        return render_template('create.html')


if __name__ == '__main__':
    initDB()
    app.run(debug=False, port=5001)
