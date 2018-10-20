from django.db import models


class Query(models.Model):
    keyword = models.CharField(max_length=100, default='DEFAULT VALUE')
    sample_size = models.IntegerField()
    language = models.CharField(max_length=100, default='DEFAULT VALUE')

    def __str__(self):
        return self.keyword


class RelevantTweet(models.Model):
    link = models.CharField(max_length=60, default='DEFAULT VALUE')
    text = models.CharField(max_length=140, default='DEFAULT VALUE')
