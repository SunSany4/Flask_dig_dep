from flask_restful import reqparse


parser = reqparse.RequestParser()

parser.add_argument('title', required=True)
parser.add_argument('content', required=True)
parser.add_argument('created_date')
parser.add_argument('is_private', required=True)
parser.add_argument('user_id', required=True)

parser.add_argument('n')
parser.add_argument('desc')