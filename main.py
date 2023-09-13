from flask import Flask, request, render_template, redirect
import random
import pymorphy2
morph = pymorphy2.MorphAnalyzer()
from data import db_session
from data.users import User
from forms.user import RegisterForm
from forms.login import LoginForm
from flask_login import LoginManager, login_user, login_required, current_user, logout_user


from handlers.login import register_login
from handlers.choice import register_choice
from handlers.index import register_index
from handlers.result import register_result
from handlers.statistics import register_statistic
from handlers.reqister import register_reqister

signup_is_on = True

app = Flask(__name__)   # Экземпляр нашего класса
login_manager = LoginManager()
login_manager.init_app(app)


app.config['SECRET_KEY'] = 'secret_key'
app.config['UPLOAD_FOLDER'] = 'static/media/from_users'
app.config['MAX_CONTENT_LENGTH'] = 128 * 1024 * 1024


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


def register_all_handlers(app: Flask):  #, login_req_arg: login_required
    register_login(app=app)
    register_choice(app=app)
    register_index(app=app)  #, login_req_arg=login_req_arg
    register_result(app=app)
    register_statistic(app=app)
    register_reqister(app=app)


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


if __name__ == "__main__":  # на другом сервере мэин не мэйн
    db_session.global_init("db/user.db")
    db_sess = db_session.create_session()
    register_all_handlers(app=app)
    app.run(host="0.0.0.0", port=8080)  # запуск локального веб сервера
