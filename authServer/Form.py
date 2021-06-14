from django import forms

from .models import not_Admin, not_Moderator


class LoginForm(forms.Form):
    login = forms.CharField(min_length=5, max_length=25, label='', widget=forms.TextInput)
    password = forms.CharField(min_length=5, max_length=25, label='', widget=forms.PasswordInput)


class new_adminForm(forms.Form):
    nick = forms.ModelChoiceField(queryset=not_Admin.objects.all())


class new_moderForm(forms.Form):
    nick = forms.ModelChoiceField(queryset=not_Moderator.objects.all())


class RegistrationForm(forms.Form):
    login = forms.CharField(max_length=100, label='',)
    password = forms.CharField(max_length=100, label='', widget=forms.PasswordInput)
    email = forms.EmailField(max_length=100, label='', widget=forms.EmailInput)
