from django.shortcuts import render
from django.http import HttpResponse
from twitmining.models import Tweets


# Create your views here.


def home(request):
    """ Exemple de page non valide au niveau HTML pour que l'exemple soit concis """
    return HttpResponse("""
        <h1>Welcome on Twitmining !</h1>
        <p>A tool for analyse a twitter feed !</p>
    """)


def tweets(request):
    list_tweets = Tweets.get_tweet('PSG')
    return HttpResponse(list_tweets)
