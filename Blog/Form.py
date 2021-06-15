from django import forms
from .models import actors, prod, styles


class FiltersForm(forms.Form):
    actor = forms.ModelChoiceField(required=False, queryset=actors.objects.all())
    producer = forms.ModelChoiceField(required=False, queryset=prod.objects.all())
    names = forms.CharField(required=False)


class FilmForm(forms.Form):
    Title = forms.CharField(max_length=100, label='', )
    actors = forms.ModelMultipleChoiceField(queryset=actors.objects.all())
    prod = forms.ModelMultipleChoiceField(queryset=prod.objects.all())
    slug = forms.SlugField(max_length=250)
    description = forms.CharField(widget=forms.Textarea)
    art_link = forms.CharField(max_length=1000, label='null', required=False)
    style = forms.ModelChoiceField(queryset=styles.objects.all())


class NewStyleForm(forms.Form):
    Name = forms.CharField(max_length=1000)


class NewNameForm(forms.Form):
    Name = forms.CharField(max_length=100, label='', widget=forms.TextInput)


class RatingForm(forms.Form):
    CHOICES = [('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')]
    like = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect, )
