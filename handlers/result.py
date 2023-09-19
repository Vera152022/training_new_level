from flask import Flask, render_template
import random
import pymorphy2
morph = pymorphy2.MorphAnalyzer()
from data import db_session
from data.users import User
from flask_login import login_required, current_user


@login_required
def result():
    print('++++++++')
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == current_user.id).first()
    good = user.result
    db_sess.commit()
    print(good, '---------+++')
    add_result(good)
    if good < 20:
        names = ['support_1', 'support_2', 'support_3', 'support_4', 'support_5']
        word = morph.parse('ошибка')[0].make_agree_with_number(20 - good).word
        res = f'Ой, у вас всего лишь {20 - good} {word}, в следующий раз все получится! Я в вас верю.'
        number = random.randint(0, 4)
        return render_template("result.html", name=names[number], text=res)
    elif good == 20:
        names = ['well_done_1', 'well_done_2', 'well_done_3', 'well_done_4', 'well_done_5']
        word = ['Вы умничка! Двигайтесь в том же направлении!!',
                        'Молодец! Двигайся в том же направлении :)',
                        'Ура, вы смогли дойти до цели!',
                        'Похоже, я вижу перед собой гения', 'Класс! Так держать!!!']
        number = random.randint(0, 4)
        number2 = random.randint(0, 4)
        return render_template("result.html", name=names[number], text=word[number2])


def add_result(good):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == current_user.id).first()
    user.all_test = str(int(user.all_test) + 1)
    if good == 20:
        user.true_test = str(int(user.true_test) + 1)
    db_sess.commit()


# def number():
#     db_sess = db_session.create_session()
#     user = db_sess.query(User).filter(User.id == current_user.id).first()
#     meaning = user.result
#     db_sess.commit()
#     return meaning


def register_result(app: Flask):
    app.add_url_rule('/result', view_func=result, methods=['GET'])