from flask import Flask, request, render_template, redirect
from data import db_session
from data.users import User
from forms.login import LoginForm
from flask_login import login_user


def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        print(99)
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


def register_login(app: Flask):
    app.add_url_rule('/login', view_func=login, methods=['GET', 'POST'])