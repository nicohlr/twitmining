from twitmining.util.search_api import CONSUMER_KEY, CONSUMER_SECRET, TOKEN, TOKEN_SECRET
import oauth2

base_url = 'https://api.twitter.com/'
timeline_id = '1052321560944611328'


def oauth_req(url, key, secret, http_method="GET", post_body="", http_headers=None):
    """

    Args:
        url (str): url of the API to request
        key (str): consumer key of the twitter application
        secret (str): consumer secret of the twitter application
        http_method (str): optional, Type of request, either GET or POST
        post_body (str): optional, post body if the request type is POST
        http_headers (dict): optional, an http header to join to the request

    Returns: The content of the request (text, status code ...)

    """
    consumer = oauth2.Consumer(key=CONSUMER_KEY, secret=CONSUMER_SECRET)
    token = oauth2.Token(key=key, secret=secret)
    client = oauth2.Client(consumer, token)
    resp, content = client.request(url, method=http_method, body=post_body, headers=http_headers)
    return content


def add_to_collection(links):
    """

    Add a list of tweets to a collection

    Args:
        links (list): links of the tweets to be added

    Returns (list): results of all the requests

    """

    result = list()

    add_collection_url_base = '{}1.1/collections/entries/add.json?'.format(base_url)

    for l in links:
        add_collection_url = add_collection_url_base + 'tweet_id=' + l.split('/status/')[
            1].strip() + '&id=custom-' + timeline_id

        add_tweet = oauth_req(add_collection_url, TOKEN, TOKEN_SECRET, http_method="POST")

        result.append(add_tweet)

    return result


def remove_from_collection(links):
    """

    Remove a list of tweets to a collection

    Args:
        links (list): links of the tweets to be removed

    Returns (list): results of all the requests

    """

    result = list()

    remove_collection_url_base = '{}1.1/collections/entries/remove.json?'.format(base_url)

    for l in links:
        remove_collection_url = remove_collection_url_base + 'tweet_id=' + l.split('/status/')[
            1].strip() + '&id=custom-' + timeline_id

        add_tweet = oauth_req(remove_collection_url, TOKEN, TOKEN_SECRET, http_method="POST")

        result.append(add_tweet)

    return result


def curate_collection(links, task="add"):
    """
    ################# NOT WORKING YET #################
    """

    result = list()

    collection_url = '{}1.1/collections/entries/curate.json?'.format(base_url)

    for l in links:

        if task == "add":
            collection_url = collection_url + 'tweet_id=' + l.split('/status/')[
                1].strip() + '&id=custom-' + timeline_id + '&op=add'
        elif task == "remove":
            collection_url = collection_url + 'tweet_id=' + l.split('/status/')[
                1].strip() + '&id=custom-' + timeline_id + '&op=remove'
        else:
            raise AttributeError("Invalid task argument, please choose between add or remove")

        add_tweet = oauth_req(collection_url, TOKEN, TOKEN_SECRET, http_method="POST")

        result.append(add_tweet)

    return result
