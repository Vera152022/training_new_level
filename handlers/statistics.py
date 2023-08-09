from flask import Flask, render_template
from data import db_session
from data.users import User
from flask_login import login_required, current_user


@login_required
def statistic():
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == current_user.id).first()
    all = user.all_test
    good = user.true_test
    db_sess.commit()
    return render_template("statistics.html", all=all, good=good)


def register_statistic(app: Flask):
    app.add_url_rule('/statistics', view_func=statistic, methods=['GET'])