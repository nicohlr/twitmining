from django.db import models
# Create your models here.


class Tweet(models.Model):
    id_number = models.CharField(max_length=30)
    text = models.CharField(max_length=140, default='DEFAULT VALUE')
    hashtags = models.CharField(max_length=140, default='DEFAULT VALUE')
    user_mentions = models.CharField(max_length=140, default='DEFAULT VALUE')
    verified = models.BooleanField(default=False)
    location = models.CharField(max_length=30, default='DEFAULT VALUE')
    link = models.CharField(max_length=60, default='DEFAULT VALUE')
    score = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return self.id_number


class RelevantTweet(models.Model):
    link = models.CharField(max_length=60, default='DEFAULT VALUE')
    score = models.PositiveSmallIntegerField(default=0)


class Keyword(models.Model):
    keyword = models.CharField(max_length=100, default='DEFAULT VALUE', verbose_name='Please enter a keyword :')

    def __str__(self):
        return self.keyword
