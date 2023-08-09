from flask import Flask, request, render_template, redirect
from data import db_session
from data.users import User
from flask_login import current_user


def choice():
    db_session.global_init("db/user.db")
    db_sess = db_session.create_session()
    if request.method == "GET":
        if current_user.is_authenticated:
            user = db_sess.query(User).filter(User.id == current_user.id).first()
            name = user.name
            db_sess.commit()
        else:
            name = 'Неизвестный гость'
        return render_template("major.html", name=name)
    elif request.method == "POST":
        print(9900)
        if request.form["choice"] == "one":
            return redirect("/lesson/1")
        if request.form["choice"] == "two":
            return redirect("/lesson/2")
        if request.form["choice"] == "three":
            return redirect("/lesson/3")
        if request.form["choice"] == "four":
            return redirect("/lesson/4")
        if request.form["choice"] == "five":
            return redirect("/lesson/5")
        if request.form["choice"] == "six":
            return redirect("/lesson/6")


def register_choice(app: Flask):
    app.add_url_rule('/', view_func=choice, methods=['GET', 'POST'])