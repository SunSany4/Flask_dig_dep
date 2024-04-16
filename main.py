from flask import Flask, render_template, redirect
from forms.loginform import LoginForm
from forms.anketa_form import AnketaForm
from forms.registerform import RegisterForm
from data import db_session
from data.users import User
from data.news import News
from datetime import datetime, timedelta
from random import randint
from flask_login import LoginManager, login_user

app = Flask(__name__)

app.config['SECRET_KEY'] = 'digitalDepartment'

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/')
@app.route('/index')
def index():
    db_session.global_init('db/blogs.db')
    db_sess = db_session.create_session()
    news = db_sess.query(News).order_by(-News.created_date)[:10]
    return render_template('index.html', news=news)


@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        pass

    return

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect('/index')
        return render_template('login.html', message='Wrong Login or password', form=form)
    return render_template('login.html', title='Authorization', form=form)


def init_data_db():
    # db_session.global_init('db/blogs.db')
    db_sess = db_session.create_session()
    # удаление всех пользователей перед заполнением таблицы
    db_sess.query(User).filter().delete()
    db_sess.query(News).filter().delete()
    db_sess.commit()

    for i in range(25):
        name = f'John{i}'
        surname = 'Doe'
        email = f'{name + surname}{i}@mail.ru'
        user = User(name=name, surname=surname, email=email)
        user.set_password('123')
        db_sess.add(user)
        title = f'News N{i}'
        content = f'{str(i) * 100}'
        created_date = datetime.now() - timedelta(days=(25 - i) * 100)
        is_private = True if i % 2 == 0 else False
        user_id = randint(1, 25)
        db_sess.add(
            News(title=title, content=content, created_date=created_date, is_private=is_private, user_id=user_id))
    db_sess.commit()
    db_sess.close()


def main():
    db_session.global_init('db/blogs.db')
    app.run()
    # init_data_db()


if __name__ == '__main__':
    main()
