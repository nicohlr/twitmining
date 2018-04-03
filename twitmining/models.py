from django.db import models
# Create your models here.


class Tweet(models.Model):
    user = models.CharField(max_length=30)
    date = models.CharField(max_length=30)
    content = models.CharField(max_length=140)
    hashtags = models.CharField(max_length=140)
    number = models.IntegerField()

    def __str__(self):
        return 'Tweet number {0}, written by {1} on {2} : {3} {4}'.format(self.number, self.user, self.date,
                                                                          self.content, self.hashtags)

