from flask import Flask, request, render_template, redirect
import random
import pymorphy2
morph = pymorphy2.MorphAnalyzer()
from data import db_session
from data.users import User
from forms.user import RegisterForm
from forms.login import LoginForm
from flask_login import LoginManager, login_user, login_required, current_user, logout_user


signup_is_on = True

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)


app.config['SECRET_KEY'] = 'secret_key'
app.config['UPLOAD_FOLDER'] = 'static/media/from_users'
app.config['MAX_CONTENT_LENGTH'] = 128 * 1024 * 1024


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route("/", methods=["GET", "POST"])
def choice():
    if request.method == "GET":
        if current_user.is_authenticated:
            user = db_sess.query(User).filter(User.id == current_user.id).first()
            name = user.name
            db_sess.commit()
        else:

            name = 'Неизвестный гость'
        return render_template("major.html", name=name)
    elif request.method == "POST":
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
        print(request.form["choice"])


tot = []
good = 0


@login_required
@app.route("/lesson/<int:site_id>", methods=["GET", "POST"])
def index1(site_id):
    global tot, good
    good = 0
    if request.method == "GET":
        if site_id == 1:
            tot = plus_minus()
        if site_id == 2:
            tot = multiplication_division()
        if site_id == 3:
            tot = plus_minus_multiplication()
        if site_id == 4:
            tot = plus_minus_division()
        if site_id == 5:
            tot = multiplication_division_2()
        if site_id == 6:
            tot = multiplication()
        return render_template("lesson.html", ans=tot[0], total=tot[1])
    elif request.method == "POST":
        cells = list(request.form.keys())
        for i in range(20):
            if str(request.form[cells[i]]) == str(tot[1][i]):
                good += 1
        print(good)
        return redirect(f"/result")


@login_required
@app.route("/result", methods=["GET"])
def result():
    global good
    add_result(good)
    if good < 20:
        names = ['support_1', 'support_2', 'support_3', 'support_4', 'support_5']
        word = morph.parse('ошибка')[0].make_agree_with_number(20 - good).word
        res = f'Ой, у вас всего лишь {20 - good} {word}, в следующий раз все получится! Я в вас верю.'
        number = random.randint(0, 4)
        return render_template("result.html", name=names[number], text=res)
    else:
        names = ['well_done_1', 'well_done_2', 'well_done_3', 'well_done_4', 'well_done_5']
        word = ['Вы умничка! Двигайтесь в том же направлении!!',
                        'Молодец! Двигайся в том же направлении :)',
                        'Ура, вы смогли дойти до цели!',
                        'Похоже, я вижу перед собой гения', 'Класс! Так держать!!!']
        number = random.randint(0, 4)
        number2 = random.randint(0, 4)
        return render_template("result.html", name=names[number], text=word[number2])


@login_required
@app.route("/statistics", methods=["GET"])
def statistic():
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == current_user.id).first()
    all = user.all_test
    good = user.true_test
    db_sess.commit()
    return render_template("statistics.html", all=all, good=good)


def add_result(good):
    good = 20
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == current_user.id).first()
    user.all_test = str(int(user.all_test) + 1)
    if good == 20:
        user.true_test = str(int(user.true_test) + 1)
    db_sess.commit()


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


def add(example, dictionary):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == current_user.id).first()
    user.example = str(example)
    user.answer = str(dictionary)
    db_sess.commit()


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


@app.route('/register', methods=['GET', 'POST'])
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
        return redirect('/')
    return render_template('register.html', title='Регистрация', form=form)


@login_required
@app.route('/logout')
def logout():
    logout_user()
    return redirect("/")


@app.errorhandler(404)
def e404(code):
    print(code)
    return render_template("error.html", err=", этой страницы не существует :)")


@app.errorhandler(500)
def e500(code):
    print(code)
    return render_template("error.html", err=", Вам необходимо зарегистрироваться")


if __name__ == "__main__":
    db_session.global_init("db/user.db")
    db_sess = db_session.create_session()
    app.run(host="0.0.0.0", port=8080)
