from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from Tagapp.models import Tag


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']


class TagForm(forms.Form):
    class Meta:
        model = Tag



