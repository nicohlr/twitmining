from django.shortcuts import render
from django.http import HttpResponse
from twitmining.models import TweetHtml
from twitmining.config import t
# Create your views here.


def home(request):
    """ Exemple de page non valide au niveau HTML pour que l'exemple soit concis """
    return HttpResponse("""
        <h1>Welcome on Twitmining !</h1>
        <p>A tool for analyse a twitter feed !</p>
    """)


def query(request):
    tweets = t.search.tweets(q="vache", count=10)
    for tweet in tweets['statuses']:
        TweetHtml.objects.create(code_html=t.statuses.oembed(_id=tweet['id'])['html'])
    data = [TweetHtml.objects.all()]
    return render(request, './twitmining/query.html', data)


def empty_database(request):
    Tweet.objects.all().delete()
    return HttpResponse("""
            <h1>The database is now empty !</h1>
        """)