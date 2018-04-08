from django import forms
from twitmining.models import Keyword

class KeywordForm(forms.ModelForm):

    class Meta:
        model = Keyword
        fields = '__all__'
