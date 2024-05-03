from flask import jsonify
from flask_restful import Resource, abort

from data import db_session
from data.news import News
from data.reqparse_news import parser


def abort_if_user_not_fount(user_id):
    session = db_session.create_session()
    users = session.query(News).get(user_id)
    if not users:
        abort(404, message=f"User {user_id} not found")


class NewsResources(Resource):
    def get(self, news_id):
        abort_if_user_not_fount(news_id)
        session = db_session.create_session()
        news = session.query(News).get(news_id)
        return jsonify({'news': news.to_dict(only=('title', 'content', 'is_private', 'created_date', 'user_id'))})

    def delete(self, news_id):
        abort_if_user_not_fount(news_id)
        session = db_session.create_session()
        news = session.query(News).get(news_id)
        session.delete(news)
        session.commit()
        return jsonify({'success': 'OK'})


class NewsListResource(Resource):
    def get(self):
        session = db_session.create_session()
        news = session.query(News).all()
        return jsonify(
            {'news': [one_news.to_dict(only=('title', 'content', 'is_private', 'created_date', 'user_id')) for one_news
             in news]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        news = News(title=args['title'], content=args['content'], is_private=args['is_private'],
                    user_id=args['user_id'])
        session.add(news)
        session.commit()
        return jsonify({'success': 'OK', 'user_id': news.id})
