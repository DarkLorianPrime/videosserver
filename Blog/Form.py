from django import forms
from .models import Actors, Prod, Styles


class FiltersForm(forms.Form):
    actor = forms.ModelChoiceField(required=False, queryset=Actors.objects.all())
    producer = forms.ModelChoiceField(required=False, queryset=Prod.objects.all())
    names = forms.CharField(required=False)


class FilmForm(forms.Form):
    Title = forms.CharField(max_length=100, label='', )
    actors = forms.ModelMultipleChoiceField(queryset=Actors.objects.all())
    prod = forms.ModelMultipleChoiceField(queryset=Prod.objects.all())
    description = forms.CharField(widget=forms.Textarea)
    art_link = forms.CharField(max_length=1000, label='null', required=False)
    style = forms.ModelChoiceField(queryset=Styles.objects.all())


class NewStyleForm(forms.Form):
    Name = forms.CharField(max_length=1000)


class NewNameForm(forms.Form):
    Name = forms.CharField(max_length=100, label='', widget=forms.TextInput)


class RatingForm(forms.Form):
    CHOICES = [[j + 1 for i in range(0, 2)] for j in range(0, 5)]
    like = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect, )
