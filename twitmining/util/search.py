import pandas as pd

class SearchEngine:
    """
    This class will perform the scoring of tweet to identify the most relevant tweets
    """

    def __init__(self, keyword, df):
        self.tweets = df
        self.keyword = keyword
        self.relevant = list()
    
    def preprocess_tweets():
        """
        This class will preprocess the dataframe by doing some actions to make easier the scoring
        """
        pass



    def score_tweets(self):
        """
        Score tweets and return the relevant list containing the most relevant tweets
        """


        for tweet in Tweet.objects.all():

            tweet.score += tweet.text.count(self.keyword)

            for hashtag in tweet.hashtags:

                if hashtag.count(self.keyword) != 0:
                    tweet.score += 2

            if tweet.user_mentions != "":
                tweet.score += 2

            if tweet.verified:
                tweet.score += 3

            if tweet.location != "":
                tweet.score += 5

            if tweet.score > 3 and tweet not in self.relevant:
                self.relevant.append(tweet)
                RelevantTweet.objects.create(
                    link=tweet.link, score=tweet.score)
