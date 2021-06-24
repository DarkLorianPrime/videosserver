from django.contrib.auth.models import User
from django.utils import timezone

from django.db import models


class Prod(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Actors(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Styles(models.Model):
    style = models.CharField(max_length=100)

    def __str__(self):
        return self.style


class Post(models.Model):
    title = models.CharField(max_length=50, default='None')
    producer = models.ManyToManyField(Prod)
    actors = models.ManyToManyField(Actors)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    description = models.TextField()
    publish = models.DateTimeField(default=timezone.now())
    author = models.CharField(max_length=100)
    style = models.ForeignKey('styles', on_delete=models.CASCADE, related_name='styles_names')

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title


class Entire_rating(models.Model):
    name = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='entire_post_name')
    entire_stars = models.FloatField()

    def __str__(self):
        return self.name


class Rating(models.Model):
    name = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='all_rating_post')
    stars = models.IntegerField()
    username = models.ForeignKey(User, on_delete=models.CASCADE, related_name='username_rater')

    def __str__(self):
        return self.name
