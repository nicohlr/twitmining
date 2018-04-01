from django.db import models
import twitmining.config as config
import requests


# Create your models here.
class Tweets(models.Model):
    user = models.CharField(max_length=30)
    date = models.DateTimeField()
    content = models.CharField(max_length=140)
    hashtags = models.CharField(max_length=140)

    def __str__(self):
        return self.date

    @staticmethod
    def get_tweet(keyword):
        tweets = []
        headers = config.search_headers
        search_params = {'q': keyword, 'result_type': 'recent', 'count': 1}
        rsp = requests.get(config.search_url, headers=headers, params=search_params).json()
        for x in rsp['statuses']:
            tweets.append({'user': x['entities']['user_mentions'][0]['screen_name'],
                           'date': x['created_at'],
                           'content': x['text'],
                           'hashtags': x['entities']['hashtags']})
        return tweets
