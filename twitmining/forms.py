from django import forms


class QueryForm(forms.Form):
    ALL = 'all'
    FRENCH = 'FR'
    SPANISH = 'ES'
    GERMAN = 'DE'
    ENGLISH = 'EN'
    LANG_CHOICES = (
        (ALL, 'All'),
        (ENGLISH, 'English'),
        (FRENCH, 'French'),
        (GERMAN, 'German'),
        (SPANISH, 'Spanish'),
    )
    keyword = forms.CharField(max_length=100, label="Keyword(s)")
    sample_size = forms.IntegerField(max_value=3000, min_value=100, initial=300, label="Sample Size",
                                     widget=forms.NumberInput(attrs={'step': '100'}))
    language = forms.ChoiceField(choices=LANG_CHOICES)
