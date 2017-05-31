from django import forms


class EntryForm(forms.Form):
    search_name = forms.BooleanField(label='Names',
                                     initial=True,
                                     required=False)
    search_mail = forms.BooleanField(label='Mails',
                                     initial=True,
                                     required=False)
    search_password = forms.BooleanField(label='Passwords',
                                         initial=True,
                                         required=False)
    search_hashword = forms.BooleanField(label='Hashwords',
                                         initial=True,
                                         required=False)
    search_website = forms.BooleanField(label='Websites',
                                        initial=True,
                                        required=False)

    entry = forms.CharField(max_length=255,
                            widget=forms.TextInput(attrs={
                                'placeholder': 'username or password or ...'
                                }))
