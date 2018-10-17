from django.contrib import admin
from .models import Keyword, RelevantTweet

admin.site.register(Keyword)
admin.site.register(RelevantTweet)