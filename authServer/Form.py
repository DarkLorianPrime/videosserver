from django import forms

from .models import not_Admin, not_Moderator, Moderator, Admin


class ModerDeleteForm(forms.Form):
    name = forms.ModelChoiceField(queryset=Moderator.objects.all())


class AdminDeleteForm(forms.Form):
    name = forms.ModelChoiceField(queryset=Admin.objects.all())


class DelUserForm(forms.Form):
    name = forms.ModelChoiceField(queryset=not_Moderator.objects.all())


class LoginForm(forms.Form):
    login = forms.CharField(max_length=100, label='', widget=forms.TextInput)
    password = forms.CharField(min_length=5, max_length=100, label='', widget=forms.PasswordInput)


class new_adminForm(forms.Form):
    nick = forms.ModelChoiceField(queryset=not_Admin.objects.all())


class new_moderForm(forms.Form):
    nick = forms.ModelChoiceField(queryset=not_Moderator.objects.all())


class RegistrationForm(forms.Form):
    login = forms.CharField(max_length=100, label='',)
    password = forms.CharField(max_length=100, label='', widget=forms.PasswordInput, min_length=5)
    email = forms.EmailField(max_length=100, label='', widget=forms.EmailInput)
