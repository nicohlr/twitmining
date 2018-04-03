from django.shortcuts import render
from django.http import HttpResponse
from twitmining.models import Tweet
import twitmining.config as config
import requests
# Create your views here.


def home(request):
    """ Exemple de page non valide au niveau HTML pour que l'exemple soit concis """
    return HttpResponse("""
        <h1>Welcome on Twitmining !</h1>
        <p>A tool for analyse a twitter feed !</p>
    """)


def tweets(request):
    headers = config.search_headers
    search_params = {'q': 'PSG', 'result_type': 'recent', 'count': 5}
    rsp = requests.get(config.search_url, headers=headers, params=search_params).json()
    count = 0
    for x in rsp['statuses']:
        Tweet.objects.create(user=x['user']['name'], date=x['created_at'],
                             content=x['text'], number=count).save()
        count += 1
    return HttpResponse(Tweet.objects.all())
    # return render(request, 'tweets.html', Tweet.objects.all())


def empty_database(request):
    Tweet.objects.all().delete()
    return HttpResponse("""
            <h1>The database is now empty !</h1>
        """)