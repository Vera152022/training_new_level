from flask import Flask, request, render_template, redirect
import random
from data import db_session
from data.users import User
from flask_login import login_required, current_user


login_reg: login_required


# Ошибка где-то в закоменченных строках


def index(site_id):
    global user_data
    if request.method == "GET":
        print(current_user, current_user.id, )
        user_data[current_user.id] = {"answers": [], "good_count": 0}
        print(user_data)
        tot = user_data[current_user.id]
        print(tot, '-----')
        if site_id == 1:
            tot["answers"] = plus_minus()
        if site_id == 2:
            tot["answers"] = multiplication_division()
        if site_id == 3:
            tot["answers"] = plus_minus_multiplication()
        if site_id == 4:
            tot["answers"] = plus_minus_division()
        if site_id == 5:
            tot["answers"] = multiplication_division_2()
        if site_id == 6:
            tot["answers"] = multiplication()
        return render_template("lesson.html", ans=tot["answers"][0])
    elif request.method == "POST":
        # user_answer(user_data[current_user.id])
        print()
        tot = user_data[current_user.id]
        cells = list(request.form.keys())
        print(request.form[cells[0]])
        print('--', cells)
        print(999999999, request.form)
        ss = []
        for i in range(20):
            ss.append(str(request.form[cells[i]]))
            print(str(request.form[cells[i]]))
            print(str(tot["answers"][1][i]))
            print('p', tot["answers"])
            if str(request.form[cells[i]]) == str(tot["answers"][1][i]):
                tot["good_count"] += 1
        print("Good", tot["good_count"])

        # user_answer(ss)
        add_result(tot["good_count"])
        tot["good_count"] = 0
        return redirect("/result")


# def user_answer(answer):
#     db_sess = db_session.create_session()
#     user = db_sess.query(User).filter(User.id == current_user.id).first()
#     user.answer_user = answer
#     db_sess.commit()


def add_result(number):
    print(number)
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == current_user.id).first()
    user.result = number
    print(user.result, '000000')

    db_sess.commit()


user_data = {}
good = 0


def plus_minus():
    example = []
    dictionary = {}
    for i in range(20):
        number = random.randint(1, 100)
        number_2 = random.randint(1, 100)
        if i % 2 == 0:
            dictionary[i] = number + number_2
            example.append(f'{number} + {number_2} = ')
        if i % 2 == 1:
            if number <= number_2:
                dictionary[i] = number_2 - number
                example.append(f'{number_2} - {number} = ')
            else:
                dictionary[i] = number - number_2
                example.append(f'{number} - {number_2} = ')
    add(example, dictionary)
    return [example, dictionary]


def multiplication_division():
    example = []
    dictionary = {}
    for i in range(20):
        number = random.randint(1, 10)
        if i % 2 == 0:
            number_2 = random.randint(1, 10)
            dictionary[i] = number * number_2
            example.append(f'{number} * {number_2} = ')
        if i % 2 == 1:
            number_2 = random.randint(1, 100)
            if number_2 % number == 0 and number <= number_2:
                dictionary[i] = number_2 // number
                example.append(f'{number_2} ÷ {number} = ')
            else:
                number_2 = number_2 + (number - (number_2 % number))
                dictionary[i] = number_2 // number
                example.append(f'{number_2} ÷ {number} = ')
    add(example, dictionary)
    return [example, dictionary]


def plus_minus_multiplication():
    example = []
    dictionary = {}
    for i in range(20):
        number = random.randint(1, 10)
        number_2 = random.randint(1, 10)
        number_3 = random.randint(1, 10)
        if i % 2 == 0:
            dictionary[i] = number_2 * number_3 + number
            example.append(f'{number} + {number_2} * {number_3} = ')
        if i % 2 == 1:
            dictionary[i] = number_2 * number_3 - number
            example.append(f'{number_2} * {number_3} - {number} = ')
    add(example, dictionary)
    return [example, dictionary]


def plus_minus_division():
    example = []
    dictionary = {}
    for i in range(20):
        number = random.randint(1, 10)
        number_2 = random.randint(1, 10)
        number_3 = random.randint(1, 10)
        if i % 2 == 1:
            if number % number_2 == 0:
                dictionary[i] = number // number_2 + number_3
                example.append(f'{number_3} + {number} ÷ {number_2} = ')
            else:
                number = number + (number_2 - (number % number_2))
                dictionary[i] = number // number_2 + number_3
                example.append(f'{number_3} + {number} ÷ {number_2} = ')
        else:
            if number % number_2 == 0:
                if number % number_2 > number_3:
                    dictionary[i] = number // number_2 - number_3
                    example.append(f'{number} ÷ {number_2} - {number_3} = ')
                else:
                    dictionary[i] = number_3 - number // number_2
                    example.append(f'{number_3} - {number} ÷ {number_2} = ')
            else:
                number = number + (number_2 - (number % number_2))
                if number % number_2 > number_3:
                    dictionary[i] = number // number_2 - number_3
                    example.append(f'{number} ÷ {number_2} - {number_3} = ')
                else:
                    dictionary[i] = number_3 - number // number_2
                    example.append(f'{number_3} - {number} ÷ {number_2} = ')
    add(example, dictionary)
    return [example, dictionary]


def multiplication_division_2():
    example = []
    dictionary = {}
    for i in range(20):
        number = random.randint(1, 10)
        number_2 = random.randint(1, 10)
        number_3 = random.randint(1, 10)
        if i % 2 == 0:
            dictionary[i] = number_2 * number_3 * number
            example.append(f'{number} * {number_2} * {number_3} = ')
        if i % 2 == 1:
            if number * number_2 % number_3 == 0:
                dictionary[i] = number * number_2 // number_3
                example.append(f'{number} * {number_2} ÷ {number_3} = ')
            else:
                number_3 = 2
                while number_3 <= number * number_2:
                    if number * number_2 % number_3 == 0:
                        break
                    else:
                        number_3 += 1
                dictionary[i] = number * number_2 // number_3
                example.append(f'{number} * {number_2} ÷ {number_3} = ')
    add(example, dictionary)
    return [example, dictionary]


def multiplication():
    example = []
    dictionary = {}
    for i in range(20):
        number = random.randint(2, 10)
        number_2 = random.randint(2, 10)
        dictionary[i] = number_2 * number
        example.append(f'{number} * {number_2} = ')
    add(example, dictionary)
    return [example, dictionary]


def add(example, dictionary):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == current_user.id).first()
    user.example = str(example)
    user.answer = str(dictionary)
    db_sess.commit()


def register_index(app: Flask):
    # login_req_arg: login_required
    # global login_reg
    # login_reg = login_req_arg
    app.add_url_rule('/lesson/<int:site_id>', view_func=index, methods=['GET', 'POST'])