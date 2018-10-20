import pandas as pd
import random
from django.shortcuts import render, redirect

from twitmining.util.search_api import get_tweets, search_url
from twitmining.util.dump import dump_on_disk
from twitmining.models import Query, RelevantTweet
from twitmining.forms import QueryForm
from twitmining.util.score import Scorer


def home(request):
    """
    Generate a form in which the user will fill the keyword(s) which will be used for the request

    Returns:
        Django.render: A render object to pass link the form to the home.html file
    """
    Query.objects.all().delete()
    
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = QueryForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            Query.objects.create(keyword=form.cleaned_data['keyword'],
                                 sample_size=form.cleaned_data['sample_size'],
                                 language=form.cleaned_data['language']
                                 ).save()

            return redirect('query')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = QueryForm()

    return render(request, './twitmining/home.html', {'form': form})


def query(request):
    """
    Create a query from keyword form

    Returns:
        Django.render: A render object to pass links of relevant tweets to the query.html file
    """

    RelevantTweet.objects.all().delete()

    assert len(Query.objects.all()) == 1

    keyword = str(Query.objects.all()[0].keyword)
    sample = Query.objects.all()[0].sample_size
    language = str(Query.objects.all()[0].language)
    Query.objects.all().delete()

    # Instantiate all variables, the dataframe will contain all tweets related to the request
    count = 0
    complete_request = dict()
    sample_request = random.randint(0, 1)
    base_url = search_url
    url = base_url
    twit_df = pd.DataFrame(columns=["id_number", "text", "hashtags",
                                    "user_mentions", "verified", "location", "link", "score"])

    # get the tweets from the twitter API, a thousand tweets maximum (10 requests * 100 tweets)
    while count < int(sample/100):

        tweets = get_tweets(url, keyword, language)

        if count == sample_request:
            sample_request = tweets['statuses'][:20]

        complete_request['request_' + str(count)] = tweets

        try:
            url = base_url + tweets['search_metadata']['next_results']
        except KeyError:
            pass

        # Process each tweet one by one by adding it to the dataframe
        for tweet in tweets['statuses']:
            
            is_retweeted = False

            try:
                place = tweet["user"]["place"]
            except KeyError:
                place = ""

            hashtags = str()

            if len(tweet["entities"]["hashtags"]) != 0:
                for hashtag in tweet["entities"]["hashtags"]:
                    hashtags = hashtags + hashtag["text"]

            hashtags = hashtags.lower()   

            if tweet["text"][:4].strip() == "RT @":
                is_retweeted = True

            keywords = keyword.split(' ')
            occurrences = 0
            occurrences_hashtags = 0
            for kw in keywords:
                occurrences += tweet["text"].count(kw)
                occurrences_hashtags += hashtags.count(kw)

            # avoid duplicate due to RT
            try:
                tweet_id = tweet["id_str"] if not is_retweeted else tweet["retweeted_status"]["id_str"]
            except KeyError:
                tweet_id = tweet["id_str"]

            setter = {"id": tweet_id,
                      "created_at": tweet["created_at"],
                      "text": tweet["text"],
                      "hashtags": hashtags,
                      "username": tweet["user"]["screen_name"],
                      "user_followers": tweet["user"]["followers_count"],
                      "verified": tweet["user"]["verified"],
                      "location": place,
                      "link": 'https://twitter.com/' + tweet["user"]["screen_name"] + '/status/' + tweet["id_str"],
                      "is_retweeted": is_retweeted,
                      "favorite_count": tweet['favorite_count'],
                      "retweet_count": tweet['retweet_count'],
                      "keyword_occurrence": occurrences,
                      "hashtag_occurrence": occurrences_hashtags,
                      "score": 0}

            twit_df = twit_df.append(setter, ignore_index=True)

        # Break the loop if all related tweets have already been found
        if len(tweets['statuses']) < 100:
            break
        else:
            count += 1

    dump_on_disk({'sample_request': sample_request})

    # drop duplicate to avoid displaying the same tweet twice using three different filters
    try:
        twit_df = twit_df.drop_duplicates(subset='text')
        twit_df = twit_df.drop_duplicates(subset='hashtags')
        twit_df = twit_df.drop_duplicates(subset='id')
    except KeyError:
        pass

    # twit_df.to_csv('twit.csv')
    twit_df["score"] = twit_df["score"].astype(str).astype(int)

    scorer = Scorer(keyword, twit_df)
    relevant = scorer.score_tweets()
    empty = True if len(relevant) == 0 else False

    col1 = relevant[:int(len(relevant)/2)]
    col2 = relevant[int(len(relevant)/2):]

    return render(request, './twitmining/query.html', {'empty': empty, 'col1': col1, 'col2': col2})
