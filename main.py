from flask import Flask, render_template, redirect
from forms.loginform import LoginForm
from forms.anketa_form import AnketaForm
from data import db_session
from data.users import User
from data.news import News

app = Flask(__name__)



app.config['SECRET_KEY'] = 'digitalDepartment'


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


def init_data_db():
    db_session.global_init('db/blogs.db')
    db_sess = db_session.create_session()
    # удаление всех пользователей перед заполнением таблицы
    db_sess.query(User).filter().delete()
    db_sess.commit()



    user = User()
    user.name = 'Alex'
    user.surname = "Popov"
    user.email = '123@123.ru'
    db_sess.add(user)
    db_sess.commit()
def main():
    # db_session.global_init('db/blogs.db')
    # app.run()
    init_data_db()



if __name__ == '__main__':
    main()
