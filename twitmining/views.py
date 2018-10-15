import pandas as pd
import requests
import random
from django.shortcuts import render, redirect

import twitmining.util.config as cg
from twitmining.util.dump import dump_on_disk
from twitmining.models import Keyword
from twitmining.forms import KeywordForm
from twitmining.util.search import SearchEngine


def home(request):
    """
    Generate a form in which the user will fill the keyword(s) which will be used for the request

    Returns:
        [type]: A render object to pass linkthe form to the home.html file
    """

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = KeywordForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            Keyword.objects.create(keyword=form.cleaned_data['keyword']).save()
            return redirect('query')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = KeywordForm()

    return render(request, './twitmining/home.html', {'form': form})


def query(request):
    """
    Create a query from keyword form

    Returns:
        Django.render: A render object to pass links of relevant tweets to the query.html file
    """

    assert len(Keyword.objects.all()) == 1

    keyword = str(Keyword.objects.all()[0])
    Keyword.objects.all().delete()

    # Instantiate all variables, the dataframe will contain all tweets related to the request
    count = 0
    complete_request = dict()
    sample_request = random.randint(0, 9)
    base_url = cg.search_url
    url = base_url
    twit_df = pd.DataFrame(columns=["id_number", "text", "hashtags",
                                    "user_mentions", "verified", "location", "link", "score"])

    # get the tweets from the twitter API, a thousand tweets maximum (10 requests * 100 tweets)
    while count < 10:

        # Twitter limits the number of tweets by request at 100
        search_params = {'q': keyword, 'result_type': 'recent', 'count': 100}

        tweets = requests.get(
            url=url, headers=cg.search_headers, params=search_params).json()

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

            if tweet["text"][:2].strip() == "RT":
                is_retweeted = True

            setter = {"id_number": tweet["id_str"],
                      "created_at": tweet["created_at"],
                      "text": tweet["text"],
                      "hashtags": hashtags,
                      "user_followers": tweet["user"]["followers_count"],
                      "verified": tweet["user"]["verified"],
                      "location": place,
                      "link": 'https://twitter.com/TheTwitmining/status/' + tweet["id_str"],
                      "is_retweeted": is_retweeted,
                      "favorite_count": tweet['favorite_count'],
                      "retweet_count": tweet['retweet_count'],
                      "score": 0}

            twit_df = twit_df.append(setter, ignore_index=True)

        # Break the loop if all related tweets have already been found
        if len(tweets['statuses']) < 100:
            break
        else:
            count += 1

    dump_on_disk({'sample_request': sample_request})

    # drop duplicate to avoid displaying the same tweet twice
    twit_df = twit_df.drop_duplicates()

    search_engine = SearchEngine(keyword, twit_df)
    relevant = search_engine.score_tweets()

    #links = [str(relevant_tweet[link]) for relevant_tweet in relevant]
    links = list()

    return render(request, './twitmining/query.html', {'links': links})
