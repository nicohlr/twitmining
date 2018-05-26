from django.db import models
# Create your models here.


class Tweet(models.Model):
    id_number = models.CharField(max_length=30)
    text = models.CharField(max_length=140)
    hashtags = models.CharField(max_length=140).choices
    user_mentions = models.CharField(max_length=140).choices
    verified = models.BooleanField()
    location = models.CharField(max_length=30)
    link = models.CharField(max_length=60)
    score = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.id_number


class RelevantTweet(models.Model):
    link = models.CharField(max_length=60)


class Keyword(models.Model):
    keyword = models.CharField(max_length=100, verbose_name='Please enter a keyword :')

    def __str__(self):
        return self.keyword
