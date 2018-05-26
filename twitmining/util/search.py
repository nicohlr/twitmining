from twitmining.models import Tweet, Keyword, RelevantTweet


class SearchEngine:

    def __init__(self):
        self.tweets = Tweet.objects.all()
        self.keyword = str(Keyword.objects.all()[0])

    def score_tweets(self):

        for tweet in Tweet.objects.all():

            tweet.score += tweet.count(self.keyword)

            for hashtag in tweet.hashtag:

                if hashtag.count(self.keyword) != 0:

                    tweet.score += 2

            if tweet.user_mentions is not None:

                tweet.score += 2

            if tweet.verified:

                tweet.score += 5

            if tweet.location != "":

                tweet.score += 5

            if tweet.score > 10:

                RelevantTweet.objects.create(link=tweet.link)