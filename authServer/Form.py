from django import forms

from .models import Role


class ModerDeleteForm(forms.Form):
    name = forms.ModelChoiceField(queryset=Role.objects.filter(name='Moderator', is_Role=True))


class AdminDeleteForm(forms.Form):
    name = forms.ModelChoiceField(queryset=Role.objects.filter(name='Administrator', is_Role=True))


class DelUserForm(forms.Form):
    name = forms.ModelChoiceField(queryset=Role.objects.exclude(name='Moderator', is_Role=True).exclude(name='Administrator', is_Role=True))


class LoginForm(forms.Form):
    login = forms.CharField(max_length=100, label='', widget=forms.TextInput)
    password = forms.CharField(min_length=5, max_length=100, label='', widget=forms.PasswordInput)


class new_adminForm(forms.Form):
    nick = forms.ModelChoiceField(queryset=Role.objects.all().filter(name='Administrator', is_Role=False))


class new_moderForm(forms.Form):
    nick = forms.ModelChoiceField(queryset=Role.objects.all().filter(name='Moderator', is_Role=False))


class RegistrationForm(forms.Form):
    login = forms.CharField(max_length=24, label='',)
    password = forms.CharField(max_length=100, label='', widget=forms.PasswordInput, min_length=5)
    email = forms.EmailField(max_length=100, label='', widget=forms.EmailInput)
