from django.db import models
# Create your models here.


class Tweet(models.Model):
    id_number = models.CharField(max_length=18)

    def __str__(self):
        return self.id_number

