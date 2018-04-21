from django import forms
from twitmining.models import Keyword


class KeywordForm(forms.Form):
    keyword = forms.CharField(max_length=100)

