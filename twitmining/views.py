from django.shortcuts import render, redirect
from twitmining.models import Tweet, Keyword, RelevantTweet
import twitmining.util.config as config
import requests
from twitmining.forms import KeywordForm
from twitmining.util.search import SearchEngine

# Create your views here.


def home(request):
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

    Tweet.objects.all().delete()
    RelevantTweet.objects.all().delete()

    assert len(Tweet.objects.all()) == 0
    assert len(RelevantTweet.objects.all()) == 0
    assert len(Keyword.objects.all()) == 1

    keyword = str(Keyword.objects.all()[0])
    Keyword.objects.all().delete()

    # get the tweets from the twitter API
    try:
        search_params = {'q': keyword, 'result_type': 'recent', 'count': 100}
        tweets = requests.get(config.search_url, headers=config.search_headers, params=search_params).json()
    except ConnectionError:
        tweets = config.t.search.tweets(q=keyword, count=100)

    # create links for displaying tweets in the html template
    for tweet in tweets['statuses']:

        try:
            place = tweet["user"]["place"]
        except KeyError:
            place = ""

        hashtags = ""
        user_mentions = ""

        for hashtag in tweet["entities"]["hashtags"]:
            hashtags = hashtags + str(hashtag["text"])

        for user_mention in tweet["entities"]["user_mentions"]:
            user_mentions = user_mentions + str(user_mention)

        Tweet.objects.create(id_number=tweet["id_str"],
                             text=tweet["text"],
                             hashtags=hashtags,
                             user_mentions=user_mentions,
                             verified=tweet["user"]["verified"],
                             location=place,
                             link='https://twitter.com/TheTwitmining/status/' + tweet["id_str"],
                             score=0).save()

    search_engine = SearchEngine(keyword)
    search_engine.score_tweets()
    links = []

    for relevant_tweet in RelevantTweet.objects.all():
        links += [str(relevant_tweet.link)]

    # clean the database for the next query
    Tweet.objects.all().delete()
    RelevantTweet.objects.all().delete()

    return render(request, './twitmining/query.html', {'links': links})
