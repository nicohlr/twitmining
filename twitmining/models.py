from django.db import models
# Create your models here.


class Tweet(models.Model):
    id_number = models.CharField(max_length=30)

    def __str__(self):
        return self.id_number


class Keyword(models.Model):
    keyword = models.CharField(max_length=100, verbose_name='Please enter a keyword :')

    def __str__(self):
        return self.keyword
