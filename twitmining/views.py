from django.shortcuts import render, redirect
from twitmining.models import Tweet, Keyword
from twitmining.config import t
from twitmining.forms import KeywordForm

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
    assert len(Tweet.objects.all()) == 0
    assert len(Keyword.objects.all()) != 0, 'putain'
    tweets = t.search.tweets(q=str(Keyword.objects.all()[0]), count=10)
    Keyword.objects.all().delete()
    links = []
    count = 0
    for tweet in tweets['statuses']:
        Tweet.objects.create(id_number=tweet['id_str']).save()
        links += ['https://twitter.com/TheTwitmining/status/' +
                  str(Tweet.objects.all()[count])]
        count += 1
    return render(request, './twitmining/query.html', {'links': links})

