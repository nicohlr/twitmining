from django.shortcuts import render
from django.http import HttpResponse
from twitmining.models import Tweet
from twitmining.config import t
# Create your views here.


def home(request):
    return render(request, 'base.html')


def query(request):
    Tweet.objects.all().delete()
    tweets = t.search.tweets(q="django", count=10)
    links = []
    count = 0
    for tweet in tweets['statuses']:
        Tweet.objects.create(id_number=tweet['id_str']).save()
        links += ['https://twitter.com/TheTwitmining/status/' +
                  str(Tweet.objects.all()[count])]
        count += 1
    return render(request, './twitmining/query.html', {'links': links})

