from django.db import models
# Create your models here.


class TweetHtml(models.Model):
    code_html = models.CharField(max_length=1000)

    def __str__(self):
        return self.code_html

