import requests

print(requests.get('http://127.0.0.1:5000/api/v2/news', json={'n':10} ).json())
