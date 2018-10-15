import twitmining.util.config as cg
import requests

url_API = "https://api.twitter.com/1.1/collections/entries/add.json"
collection_id = '1051915299279253510'
tweet_id = '1051895052467888131'
post_params = {'id': collection_id, 'tweet_id': tweet_id}

collection = requests.post(
            url=url_API, headers=cg.search_headers, params=post_params).json()

# https://twitter.com/TheTwitmining/timelines/1051915299279253510?ref_src=twsrc%5Etfw