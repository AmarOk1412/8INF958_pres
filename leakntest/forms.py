from django import forms


class EntryForm(forms.Form):
    entry = forms.CharField(max_length=255)
