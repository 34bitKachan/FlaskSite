from flask import Flask, render_template, request, redirect, url_for
from database.create import initDB
from database.request_DB import add_article, get_articles

app = Flask(__name__)


@app.route("/")
def hello_world():
    return render_template('index.html')


@app.route("/about")
def about():
    return render_template('about.html')


@app.route("/reg", methods=["GET", ])
def registration_user():
    return render_template('registration/reg.html')


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
