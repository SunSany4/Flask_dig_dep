import flask
from . import db_session
from .news import News
from flask import jsonify, make_response, request

blueprint = flask.Blueprint('news_api', __name__, template_folder='templates')


@blueprint.route('/api/news')
def get_news():
    db_sess = db_session.create_session()
    news = db_sess.query(News).all()
    return jsonify({'news': [item.to_dict(only=('title', 'content', 'user.name')) for item in news]})


@blueprint.route('/api/news/<int:news_id>', methods=['GET'])
def get_one_news(news_id):
    db_sess = db_session.create_session()
    news = db_sess.query(News).get(news_id)
    if not news:
        return make_response(jsonify({'error': 'Not Found'}), 404)
    return jsonify({'news': news.to_dict(only=('title', 'content', 'user.name'))})


@blueprint.route('/api/news_delete/<int:news_id>', methods=['DELETE'])
def delete_one_news(news_id):
    db_sess = db_session.create_session()
    news = db_sess.query(News).get(news_id)
    if not news:
        return make_response(jsonify({'error': 'Not Found'}), 404)
    db_sess.delete(news)
    db_sess.commit()
    return jsonify({'status': 'OK'})


@blueprint.route('/api/news', methods=['POST'])
def add_one_news():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in ['title', 'content', 'is_private', 'user_id']):
        return jsonify({'error': 'Bad request'})
    db_sess = db_session.create_session()
    news = News(
        title=request.json['title'],
        content=request.json['content'],
        is_private=request.json['is_private'],
        user_id=request.json['user_id'],
    )

    db_sess.add(news)
    db_sess.commit()
    return jsonify({'status': 'OK'})


"""
написать обработчик для удаления новости  (DELETE)
и для добавления новости (POST)
"""
