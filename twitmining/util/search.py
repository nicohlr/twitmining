from twitmining.models import RelevantTweet


class SearchEngine:
    """
    This class will perform the scoring of tweet to identify the most relevant tweets
    """

    def __init__(self, keyword, df):
        self.tweets = df
        self.keyword = keyword
        self.relevant = list()

    def score_retweets(self):
        for index, tweet in self.tweets.iterrows():
            if tweet["is_retweeted"]:
                self.tweets.at[index, "score"] = int(tweet['score'] - 200)
    
    def score_occurrences(self):
        for index, tweet in self.tweets.iterrows():
            self.tweets.at[index, "score"] = int(tweet['score'] + tweet["keyword_occurrence"]*100)

    def score_user(self):
        for index, tweet in self.tweets.iterrows():
            self.tweets.at[index, "score"] = int(tweet['score'] + tweet["user_followers"]/100)
            if tweet["verified"]:
                self.tweets.at[index, "score"] = int(tweet['score'] + 100)

    def score_sharing(self):
        for index, tweet in self.tweets.iterrows():
            self.tweets.at[index, "score"] = int(tweet['score'] + tweet["favorite_count"])
            self.tweets.at[index, "score"] = int(tweet['score'] + tweet["retweet_count"])

    def score_tweets(self):
        """
        Score tweets and return the relevant list containing the most relevant tweets
        """

        self.score_occurrences()
        self.score_retweets()
        self.score_sharing()
        self.score_user()

        relevant = self.tweets.nlargest(10, "score")
        relevant_links = list()

        for index, tweet in relevant.iterrows():
            relevant_links.append(self.tweets.at[index, 'link'])
            RelevantTweet.objects.create(link=self.tweets.at[index, 'link'], text=self.tweets.at[index, 'text'])

        return relevant_links
