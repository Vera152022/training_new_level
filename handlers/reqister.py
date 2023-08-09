from flask import Flask, render_template, redirect
from data import db_session
from data.users import User
from forms.user import RegisterForm
from flask_login import login_user


def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User()
        user.name = form.name.data
        user.about = form.about.data
        user.email = form.email.data
        user.set_password(form.password.data)
        user.all_test = '0'
        user.true_test = '0'
        db_sess = db_session.create_session()
        db_sess.add(user)
        db_sess.commit()
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        login_user(user)
        return redirect('/')
    return render_template('register.html', form=form)


def register_reqister(app: Flask):
    app.add_url_rule('/register', view_func=reqister, methods=['GET', 'POST'])