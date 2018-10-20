import requests
import base64
import os

passwords = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'passwords.txt'))

CONSUMER_KEY = passwords.readline()[:-1]
CONSUMER_SECRET = passwords.readline()[:-1]
TOKEN = passwords.readline()[:-1]
TOKEN_SECRET = passwords.readline()[:-1]

# using requests module
key_secret = '{}:{}'.format(CONSUMER_KEY, CONSUMER_SECRET).encode('ascii')
b64_encoded_key = base64.b64encode(key_secret)
b64_encoded_key = b64_encoded_key.decode('ascii')

base_url = 'https://api.twitter.com/'
auth_url = '{}oauth2/token'.format(base_url)

auth_headers = {'Authorization': 'Basic {}'.format(b64_encoded_key),
                'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'}
auth_resp = requests.post(auth_url, headers=auth_headers, data={'grant_type': 'client_credentials'})
access_token = auth_resp.json()['access_token']

search_headers = {'Authorization': 'Bearer {}'.format(access_token)}
search_url = '{}1.1/search/tweets.json'.format(base_url)


def get_tweets(url, keyword, language='all'):
    # Twitter limits the number of tweets by request at 100
    if language != 'all':
        search_params = {'q': keyword, 'result_type': 'recent', 'count': 100, 'lang': language}
    else:
        search_params = {'q': keyword, 'result_type': 'recent', 'count': 100}
    return requests.get(url=url, headers=search_headers, params=search_params).json()
