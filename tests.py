import requests

print(requests.post('http://127.0.0.1:5000/api/v2/users', json={'name': 'Title1',
                                                               'surname': 'dffsgfds',
                                                               'email': '12@21.ru',
                                                               'hashed_password': '123',
                                                               }).json())
