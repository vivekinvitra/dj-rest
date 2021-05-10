from django import forms
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import request


class SearchForm(forms.Form):
    query = forms.CharField(label='Search', max_length=100)
    catid = forms.IntegerField()


class SignUpForm(UserCreationForm):
    username = forms.CharField(max_length=30, label='User Name', widget=forms.TextInput(attrs={'class': "bo-rad-10 sizefull txt10 p-l-20"}))
    email = forms.EmailField(max_length=200, label='E-mail', widget=forms.TextInput(attrs={'class': "bo-rad-10 sizefull txt10 p-l-20"}))
    first_name = forms.CharField(max_length=100, label='First Name', widget=forms.TextInput(attrs={'class': "bo-rad-10 sizefull txt10 p-l-20"}))
    last_name = forms.CharField(max_length=100, label='Last Name', widget=forms.TextInput(attrs={'class': "bo-rad-10 sizefull txt10 p-l-20"}))
    password1 = forms.CharField(max_length=100, label='Password', widget=forms.PasswordInput(attrs={'class': "bo-rad-10 sizefull txt10 p-l-20"}))
    password2 = forms.CharField(max_length=100, label='Password Confirmation', widget=forms.PasswordInput(attrs={'class': "bo-rad-10 sizefull txt10 p-l-20"}))

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']