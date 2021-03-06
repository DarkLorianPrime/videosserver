from django import forms

from .models import Role, Role_List


class ModerDeleteForm(forms.Form):
    name = forms.ModelChoiceField(queryset=Role.objects.filter(name=4))


class AdminDeleteForm(forms.Form):
    name = forms.ModelChoiceField(queryset=Role.objects.filter(name=3))


class DelUserForm(forms.Form):
    name = forms.ModelChoiceField(queryset=Role.objects.filter(name=2))


class LoginForm(forms.Form):
    login = forms.CharField(max_length=100, label='', widget=forms.TextInput)
    password = forms.CharField(min_length=5, max_length=100, label='', widget=forms.PasswordInput)


class new_adminForm(forms.Form):
    nick = forms.ModelChoiceField(queryset=Role.objects.filter(name=4))


class new_moderForm(forms.Form):
    nick = forms.ModelChoiceField(queryset=Role.objects.filter(name=2))


class RegistrationForm(forms.Form):
    login = forms.CharField(max_length=24, label='',)
    password = forms.CharField(max_length=100, label='', widget=forms.PasswordInput, min_length=5)
    email = forms.EmailField(max_length=100, label='', widget=forms.EmailInput)
