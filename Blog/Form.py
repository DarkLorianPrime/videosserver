from django import forms
from .models import Styles


class RecentForm(forms.Form):
    emails = forms.EmailField()


class local_ResetForm(forms.Form):
    name = forms.CharField(widget=forms.PasswordInput)


class ResetForm(forms.Form):
    name = forms.CharField(widget=forms.PasswordInput)
    new_name = forms.CharField(widget=forms.PasswordInput)


class FiltersForm(forms.Form):
    names = forms.CharField(required=False)


class FilmForm(forms.Form):
    Title = forms.CharField(max_length=100, label='', )
    description = forms.CharField(widget=forms.Textarea)
    style = forms.ModelChoiceField(queryset=Styles.objects.all())


class NewStyleForm(forms.Form):
    Name = forms.CharField(max_length=1000)


class RatingForm(forms.Form):
    CHOICES = [[j + 1 for i in range(0, 2)] for j in range(0, 5)]
    like = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect, )
