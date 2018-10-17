from twitmining.util.config import CONSUMER_KEY, CONSUMER_SECRET, TOKEN, TOKEN_SECRET
import oauth2

base_url = 'https://api.twitter.com/'
timeline_id = '1052321560944611328'


def oauth_req(url, key, secret, http_method="GET", post_body="", http_headers=None):
    consumer = oauth2.Consumer(key=CONSUMER_KEY, secret=CONSUMER_SECRET)
    token = oauth2.Token(key=key, secret=secret)
    client = oauth2.Client(consumer, token)
    resp, content = client.request(url, method=http_method, body=post_body, headers=http_headers)
    return content


def add_to_collection(links):

    result = list()

    add_collection_url_base = '{}1.1/collections/entries/add.json?'.format(base_url)

    for l in links:
        add_collection_url = add_collection_url_base + 'tweet_id=' + l.split('/status/')[1] + '&id=custom-' + timeline_id

        add_tweet = oauth_req(add_collection_url, TOKEN, TOKEN_SECRET, http_method="POST")

        result.append(add_tweet)

    return result


def remove_from_collection(links):

    result = list()

    remove_collection_url_base = '{}1.1/collections/entries/remove.json?'.format(base_url)

    for l in links:
        remove_collection_url = remove_collection_url_base + 'tweet_id=' + l.split('/status/')[
            1] + '&id=custom-' + timeline_id

        add_tweet = oauth_req(remove_collection_url, TOKEN, TOKEN_SECRET, http_method="POST")

        result.append(add_tweet)

    return result
