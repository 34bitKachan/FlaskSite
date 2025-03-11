from flask import Flask, render_template, request, redirect, url_for, session, make_response, flash
from database.create import initDB
from database.request_DB import add_article, get_articles, add_user, get_user_login, updateUserAvatar
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required,logout_user, current_user
from UserLogin import UserLogin
from forms import LoginForm

from admin.admin import admin

MAX_CONTENT_USER = 1024 * 1024
app = Flask(__name__)
app.config['SECRET_KEY'] = 'bbc8c139920f6e04392498074514b5376ad0e615'
app.register_blueprint(admin, url_prefix='/admin')


login_manager = LoginManager(app)
login_manager.login_view = 'login'




@app.route("/")
def index():
    if 'visits' in session:
        session['visits'] = session.get('visits') + 1
    else:
        session['visits'] = 1
    return render_template('index.html', mes=session['visits'])

#
# @app.route("/session")
# def session_get():
#     data = [1, 2, 3, 4]
#     session.permanent = True
#     if 'dat' not in session:
#         session['dat'] = data
#     else:
#         session['dat'][1] += 1
#         session.modified = True
#     return f"session['dat']:: {session['dat']}"


@app.route("/about")
def about():
    return render_template('about.html')


@app.route("/reg", methods=["POST", "GET"])
def registration_user():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        password = generate_password_hash(password=password)
        if username != "" and email != "" and password != "":
            is_create = add_user(username=username, password=password, email=email)
            if is_create:
                return redirect('/')
            return render_template('registration/reg.html', mes="Имя пользователя занято")
        return render_template('registration/reg.html', mes="Заполните все поля!")
    return render_template('registration/reg.html')


@app.route("/profile", methods=["POST", "GET"])
def profile():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    return render_template('profile.html')


@app.route("/sing_in", methods=["POST", "GET"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    # if request.method == "POST":
    #     username = request.form.get("username")
    #     password = request.form.get("password")
    #     if username != "" and password != "":
    #         user = get_user_login(username=username)
    #         if not user:
    #             return render_template('registration/sing_in.html', mes="Неправильный логин или пароль")
    #         if check_password_hash(user['password'], password):
    #             from UserLogin import UserLogin
    #             userlogin = UserLogin().create(user)
    #             login_user(userlogin)
    #             print(user['username'])
    #             return redirect(request.args.get('next') or url_for("profile"))
    #         return render_template('registration/sing_in.html', mes="Неправильный логин или пароль")
    #     return render_template('registration/sing_in.html', mes="Заполните все поля!")
    # return render_template('registration/sing_in.html')

    form = LoginForm()
    if form.validate_on_submit():
        print("validate")
        username = form.email.data
        password = form.psw.data
        if username != "" and password != "":
            user = get_user_login(username=username)
            if not user:
                return render_template('registration/sing_in.html', mes="Неправильный логин или пароль")
            if check_password_hash(user['password'], password):
                from UserLogin import UserLogin
                userlogin = UserLogin().create(user)
                login_user(userlogin)
                print(user['username'])
                return redirect(request.args.get('next') or url_for("profile"))
            return render_template('registration/sing_in.html', mes="Неправильный логин или пароль")
        return render_template('registration/sing_in.html', mes="Заполните все поля!")
    return render_template('registration/sing_in.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')

@app.route("/article")
def get_article():
    print(get_articles())
    return render_template('article.html', posts=get_articles())

@app.route("/userava")
@login_required
def userava():
    img = current_user.getAvatar(app=app)
    if not img:
        return ""
    h = make_response(img)
    h.headers['Content-Type'] = 'image/png'
    return h

@app.route('/upload', methods=["POST", "GET"])
@login_required
def upload():
    if request.method == "POST":
        file = request.files['file']
        if file and current_user.verifyExt(file.filename):
            try:
                img = file.read()
                res = updateUserAvatar(img, current_user.get_id())
                if not res:
                    flash("Error update avatar", "error")
                    return redirect('/profile')
                flash("Error update avatar", "success")
            except FileNotFoundError as e:
                flash("Error read file", "error")
        else:
            flash("error update avatar", "error")
    return redirect(url_for('profile'))


@app.route("/create", methods=["POST", "GET"])
@login_required
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
@login_manager.user_loader
def load_user(user_id):
    print(user_id)
    print("load_user")
    return UserLogin().fromDB(user_id)

if __name__ == '__main__':
    initDB()
    app.run(debug=True, host='0.0.0.0',port=5001)
