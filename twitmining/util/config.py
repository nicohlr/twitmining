from twitter import *
import requests
import base64

_CONSUMER_KEY = '68PIz9Q117DEvM8wsZAXUgPW6'
_CONSUMER_SECRET = 'RK0kxlCaJM5HEUTXITXgJd9ZAtGed4M1OeCBOihJkGr5jjLRhP'
_TOKEN = '980475833314836480-l0EzfWGZbvYQVtSqmbj2syQ2WRELkA8'
_TOKEN_SECRET = '5kunx2UHEVOJubNG3zzo0ZhdW8g4HS4270Rg2X6qSwC7o'

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
access_token = auth_resp.json()['access_token']

search_headers = {'Authorization': 'Bearer {}'.format(access_token)}
search_url = '{}1.1/search/tweets.json'.format(base_url)
