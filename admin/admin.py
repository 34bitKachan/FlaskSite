from flask import Blueprint, request, redirect, url_for, render_template, flash, session

admin = Blueprint('admin', __name__, template_folder='templates', static_folder='static')


def login_admin():
    session['admin_logged'] = 1


def isLogged():
    return True if session.get('admin_logged') else False


def logout_admin():
    session.pop('admin_logged', None)


@admin.route('/')
def index():
    if not isLogged():
        return redirect(url_for('.login'))
    return render_template('admin.html')

@admin.route("/login", methods=["POST", "GET"])
def login():
    if isLogged():
        return redirect(url_for('.index'))
    if request.method == "POST":
        if request.form['username'] == 'admin' and request.form['psw'] == "1234":
            login_admin()
            return redirect(url_for('.index'))
        else:
            flash("Неверный логин или пароль", "error")
    return render_template('login.html')


@admin.route("/logout", methods=["POST", "GET"])
def logout():
    if not isLogged():
        return redirect(url_for('.login'))

    logout_admin()
    return render_template('login.html')
