import requests
import base64

client_key = '2v3phi7u2OIcKPLwZm7oGfbXZ'
client_secret ='Tm5iT4uC0os4u6TrqEJSAT5nW7hqnoFBsKAVEOrpwGoqsMSUk8'


key_secret = '{}:{}'.format(client_key, client_secret).encode('ascii')
b64_encoded_key = base64.b64encode(key_secret)
b64_encoded_key = b64_encoded_key.decode('ascii')


base_url = 'https://api.twitter.com/'
auth_url = '{}oauth2/token'.format(base_url)

auth_headers = {
    'Authorization': 'Basic {}'.format(b64_encoded_key),
    'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
}

auth_data = {
    'grant_type': 'client_credentials'
}

auth_resp = requests.post(auth_url, headers=auth_headers, data=auth_data)

access_token = auth_resp.json()['access_token']

search_headers = {
    'Authorization': 'Bearer {}'.format(access_token)
}

search_url = '{}1.1/search/tweets.json'.format(base_url)
