import pandas as pd
import random
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


from twitmining.util.search_api import get_tweets, search_url
from twitmining.util.dump import dump_on_disk
from twitmining.models import Query, RelevantTweet
from twitmining.forms import QueryForm, ConnectionForm, InscriptionForm, MailForm
from twitmining.util.score import Scorer
from twitmining.util.preprocessing import preprocess_tweet
from twitmining.util.mail import send_mail
from socialmining.settings import DEBUG


def log_in(request):
    """
    View for the root page, allows user to sign in to access the website
    """

    error = False

    if request.method == "POST":
        form = ConnectionForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)  # check if data are valid
            if user:
                login(request, user)
                return redirect('home')
            else:
                error = True

    else:
        if request.user.is_authenticated:
            return redirect('home')
        else:
            form = ConnectionForm()

    return render(request, './twitmining/login.html', {'form': form, 'error': error})


def log_out(request):
    """
    View for the logout page
    """
    logout(request)
    return redirect('/')


def sign_up(request):
    """
    View for the signup page, allows user to create an account
    """
    password_error = False
    email_error = False
    username_error = False
    error = False

    if request.method == "POST":
        form = InscriptionForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data["email"]
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            confirmed_password = form.cleaned_data["confirmed_password"]

            if User.objects.filter(email=email).exists():
                email_error = True
            if User.objects.filter(username=username).exists():
                username_error = True
            if password != confirmed_password:
                password_error = True

            if not password_error and not username_error and not email_error:
                User.objects.create_user(username=username, password=password, email=email)
                user = authenticate(username=username, password=password)
                login(request, user)
                return redirect('home')

    else:
        if request.user.is_authenticated:
            return redirect('home')
        else:
            form = InscriptionForm()

    error = True if password_error or email_error or username_error else False

    return render(request, './twitmining/signup.html', {'form': form,
                                                        'error': error,
                                                        'username_error': username_error,
                                                        'email_error': email_error,
                                                        'password_error': password_error})


@login_required(login_url='/')
def home(request):
    """
    Generate a form in which the user will fill the keyword(s) which will be used for the request

    Returns:
        Django.render: A render object to pass link the form to the home.html file
    """
    Query.objects.all().delete()
    sending_confirmation = False

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form_search = QueryForm(request.POST)
        form_email = MailForm(request.POST)
        # check whether it's valid:
        if form_search.is_valid():
            Query.objects.create(keyword=form_search.cleaned_data['keyword'],
                                 sample_size=form_search.cleaned_data['sample_size'],
                                 language=form_search.cleaned_data['language']
                                 ).save()

            return redirect('query')
        
        if form_email.is_valid():
            name = form_email.cleaned_data["name"]
            email = form_email.cleaned_data["email"]
            message = form_email.cleaned_data["message"]
            
            sending_confirmation = send_mail(email, name, message)
            return render(request, './twitmining/home.html', {'form_search': QueryForm(),
                                                              'form_email': MailForm(),
                                                              'sending_confirmation': sending_confirmation,
                                                              'debug': DEBUG})

    # if a GET (or any other method) we'll create a blank form
    else:
        form_search = QueryForm()
        form_email = MailForm()

    return render(request, './twitmining/home.html', {'form_search': form_search,
                                                      'form_email': form_email,
                                                      'sending_confirmation': sending_confirmation,
                                                      'debug': DEBUG})


@login_required(login_url='/')
def query(request):
    """
    Create a query from keyword form

    Returns:
        Django.render: A render object to pass links of relevant tweets to the query.html file
    """

    RelevantTweet.objects.all().delete()

    keyword = str(Query.objects.all()[0].keyword)
    sample = Query.objects.all()[0].sample_size
    language = str(Query.objects.all()[0].language)

    # Instantiate all variables, the dataframe will contain all tweets related to the request
    count = 0
    complete_request = dict()
    sample_request = random.randint(0, 1)
    base_url = search_url
    url = base_url
    twit_df = pd.DataFrame(columns=["id", "created_at", "text", "hashtags", "username", "user_followers",
                                    "verified", "location", "link", "is_retweeted", "favorite_count",
                                    "retweet_count", "keyword_occurrence", "hashtag_occurrence",
                                    "has_media", "score"])

    # get the tweets from the twitter API, a thousand tweets maximum (10 requests * 100 tweets)
    while count < int(sample/100):

        tweets = get_tweets(url, keyword, language)

        if count == sample_request and DEBUG:
            sample_request = tweets['statuses'][:20]

        complete_request['request_' + str(count)] = tweets

        if 'next_results' in tweets['search_metadata']:
            url = base_url + tweets['search_metadata']['next_results']

        # Process each tweet one by one by adding it to the dataframe
        for tweet in tweets['statuses']:
            setter = preprocess_tweet(tweet=tweet, keyword=keyword)
            twit_df = twit_df.append(setter, ignore_index=True)

        # Break the loop if all related tweets have already been found
        if len(tweets['statuses']) < 100:
            break
        else:
            count += 1

    if DEBUG:
        dump_on_disk({'sample_request': sample_request})

    # drop duplicate to avoid displaying the same tweet twice using three different filters
    twit_df = twit_df.drop_duplicates(subset='text')
    twit_df = twit_df.drop_duplicates(subset='hashtags')
    twit_df = twit_df.drop_duplicates(subset='id')

    # twit_df.to_csv('twit.csv')
    twit_df["score"] = twit_df["score"].astype(str).astype(int)

    scorer = Scorer(keyword, twit_df)
    relevant = scorer.score_tweets()
    empty = True if len(relevant) == 0 else False

    col1 = relevant[:int(len(relevant)/2)]
    col2 = relevant[int(len(relevant)/2):]

    return render(request, './twitmining/query.html', {'empty': empty, 'col1': col1, 'col2': col2})
