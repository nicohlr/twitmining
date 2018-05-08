from twitter import *
import requests
import base64
import os

passwords = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'passwords.txt'))

_CONSUMER_KEY = passwords.readline()[:-1]
_CONSUMER_SECRET = passwords.readline()[:-1]
_TOKEN = passwords.readline()[:-1]
_TOKEN_SECRET = passwords.readline()[:-1]

# using twitter module
t = Twitter(auth=OAuth(_TOKEN, _TOKEN_SECRET, _CONSUMER_KEY, _CONSUMER_SECRET))

# using requests module
key_secret = '{}:{}'.format(_CONSUMER_KEY, _CONSUMER_SECRET).encode('ascii')
b64_encoded_key = base64.b64encode(key_secret)
b64_encoded_key = b64_encoded_key.decode('ascii')

base_url = 'https://api.twitter.com/'
auth_url = '{}oauth2/token'.format(base_url)

auth_headers = {'Authorization': 'Basic {}'.format(b64_encoded_key),
                'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'}
auth_resp = requests.post(auth_url, headers=auth_headers, data={'grant_type': 'client_credentials'})
print(auth_resp)
access_token = auth_resp.json()['access_token']

search_headers = {'Authorization': 'Bearer {}'.format(access_token)}
search_url = '{}1.1/search/tweets.json'.format(base_url)
