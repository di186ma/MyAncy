from django import forms


class WayForm(forms.Form):
    start = forms.CharField(label='start', max_length=100)
    finish = forms.CharField(label='finish', max_length=100)
