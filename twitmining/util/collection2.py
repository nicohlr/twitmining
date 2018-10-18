from TwitterAPI import TwitterAPI
from twitmining.util.config import CONSUMER_KEY, CONSUMER_SECRET, TOKEN, TOKEN_SECRET


api = TwitterAPI(CONSUMER_KEY, CONSUMER_SECRET, TOKEN, TOKEN_SECRET)

a = {"id": "custom-755492810149683200", "changes": [{"op": "add", "tweet_id": "710205975505063937"}]}


r = api.request('collections/entries/curate', a)

print(r.status_code, r.text)
