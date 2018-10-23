def preprocess_tweet(tweet, keyword):

    has_media = False
    is_retweeted = False

    location = tweet["user"]["place"] if "place" in tweet["user"] else None

    hashtags = str()
    if len(tweet["entities"]["hashtags"]) != 0:
        for hashtag in tweet["entities"]["hashtags"]:
            hashtags = hashtags + hashtag["text"]

    if tweet["text"][:4].strip() == "RT @":
        is_retweeted = True

    if 'media' in tweet["entities"]:
        has_media = True

    keywords = keyword.split(' ')
    occurrences = 0
    occurrences_hashtags = 0
    for kw in keywords:
        occurrences += tweet["text"].lower().count(kw.lower())
        occurrences_hashtags += hashtags.lower().count(kw.lower())

    # avoid duplicate due to RT
    if "retweeted_status" in tweet:
        tweet_id = tweet["id_str"] if not is_retweeted else tweet["retweeted_status"]["id_str"]
    else:
        tweet_id = tweet["id_str"]

    setter = {"id": tweet_id,
              "created_at": tweet["created_at"],
              "text": tweet["text"],
              "hashtags": hashtags,
              "username": tweet["user"]["screen_name"],
              "user_followers": tweet["user"]["followers_count"],
              "verified": tweet["user"]["verified"],
              "location": location,
              "link": 'https://twitter.com/' + tweet["user"]["screen_name"] + '/status/' + tweet["id_str"],
              "is_retweeted": is_retweeted,
              "favorite_count": tweet['favorite_count'],
              "retweet_count": tweet['retweet_count'],
              "keyword_occurrence": occurrences,
              "hashtag_occurrence": occurrences_hashtags,
              "has_media": has_media,
              "score": 0}
    
    return setter
        