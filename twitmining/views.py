from django.shortcuts import render
from django.http import HttpResponse
from twitmining.models import Tweet
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
    links = []
    count = 0
    for tweet in tweets['statuses']:
        Tweet.objects.create(id_number=tweet['id_str']).save()
        links += ['https://twitter.com/TheTwitmining/status/' + str(Tweet.objects.all()[count])]
        count += 1
    return render(request, './twitmining/query.html', {'links': links})


def empty_database(request):
    Tweet.objects.all().delete()
    return HttpResponse("""
            <h1>The database is now empty !</h1>
        """)