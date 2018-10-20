from django import forms


class QueryForm(forms.Form):
    keyword = forms.CharField(max_length=100, label="Keyword(s)")
    sample_size = forms.IntegerField(max_value=3000, min_value=100, initial=300, label="Sample Size",
                                     widget=forms.NumberInput(attrs={'step': '100'}))
