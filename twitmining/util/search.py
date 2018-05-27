from twitmining.models import Tweet, RelevantTweet


class SearchEngine:

    def __init__(self, keyword):
        self.tweets = Tweet.objects.all()
        self.keyword = keyword

    def score_tweets(self):

        for tweet in Tweet.objects.all():

            tweet.score += tweet.text.count(self.keyword)

            for hashtag in tweet.hashtags:

                if hashtag.count(self.keyword) != 0:

                    tweet.score += 2

            if tweet.user_mentions is not None:

                tweet.score += 2

            if tweet.verified:

                tweet.score += 5

            if tweet.location != "":

                tweet.score += 5

            if tweet.score > 5:

                RelevantTweet.objects.create(link=tweet.link, score=tweet.score)
