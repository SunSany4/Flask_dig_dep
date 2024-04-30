from flask import Flask, render_template, redirect, url_for, abort, request
from forms.loginform import LoginForm
from forms.newsform import NewsForm
from forms.registerform import RegisterForm
from data import db_session, news_api
from data.users import User
from data.news import News

from datetime import datetime, timedelta
from random import randint
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from flask_restful import reqparse, abort, Api, Resource
from data import users_resources

app = Flask(__name__)
api = Api(app)

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
    news = db_sess.query(News).order_by(News.created_date.desc())[:10]
    return render_template('index.html', news=news)


@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html',
                                   title='Регистрация',
                                   form=form,
                                   message='Пароли не совпадают')
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html',
                                   title='Регистрация',
                                   form=form,
                                   message='Пользователь с таким адресом почты уже существует')
        user = User(
            name=form.name.data,
            surname=form.surname.data,
            email=form.email.data,
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html',
                           title='Регистрация',
                           form=form,
                           )


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


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/index')


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


@app.route('/news', methods=['GET', 'POST'])
@login_required
def add_news():
    form = NewsForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        news = News()
        news.title = form.title.data
        news.content = form.content.data
        news.is_private = form.is_private.data
        current_user.news.append(news)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/index')

    return render_template('news.html', title='Добавление новости', form=form)


@app.route('/news/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_news(id):
    form = NewsForm()
    if request.method == 'GET':
        db_sess = db_session.create_session()
        news = db_sess.query(News).filter(News.id == id, News.user == current_user).first()
        if news:
            form.title.data = news.title
            form.content.data = news.content
            form.is_private.data = news.is_private
        else:
            abort(404)

    if form.validate_on_submit():
        db_sess = db_session.create_session()
        news = db_sess.query(News).filter(News.id == id, News.user == current_user).first()
        if news:
            news.title = form.title.data
            news.content = form.content.data
            news.is_private = form.is_private.data
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('news.html', title='Редактирование новости', form=form)

@app.route('/news_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def news_delete(id):
    db_sess = db_session.create_session()
    news = db_sess.query(News).filter(News.id == id, News.user == current_user).first()
    if news:
        db_sess.delete(news)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')




def main():
    db_session.global_init('db/blogs.db')
    api.add_resource(users_resources.UsersResources, '/api/v2/users/<int:user_id>')
    api.add_resource(users_resources.UsersListResource, '/api/v2/users')
    # app.register_blueprint(news_api.blueprint)
    app.run()
    # init_data_db()


if __name__ == '__main__':
    main()
