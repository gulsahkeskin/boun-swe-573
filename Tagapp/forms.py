import requests
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from wikiFile import WikiData


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']


suggestion_list = WikiData.wiki_suggest(query="bipolar disorder")
# print(choices)


class TagForm(forms.Form):
    # search = forms.MultipleChoiceField(choices=suggestion_list)
    search = forms.CharField()
    name = forms.CharField(help_text='your custom name for tag')
    botcathcer = forms.CharField(required=False,
                                 widget=forms.HiddenInput)



