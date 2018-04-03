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
    search_params = {'q': 'PSG', 'result_type': 'recent', 'count': 1}
    rsp = requests.get(config.search_url, headers=headers, params=search_params).json()
    for x in rsp['statuses']:
        Tweet.objects.create(user=x['user']['name'], date=x['created_at'],
                             content=x['text'], number=0).save()
    return HttpResponse(Tweet.objects.all())
