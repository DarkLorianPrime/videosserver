from django.utils import timezone

from django.db import models


class prod(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class actors(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class rating(models.Model):
    name = models.CharField(max_length=100)
    stars = models.IntegerField()
    username = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class styles(models.Model):
    style = models.CharField(max_length=100)

    def __str__(self):
        return self.style


class Post(models.Model):
    title = models.CharField(max_length=50)
    producer = models.JSONField()
    actors = models.JSONField()
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    description = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    author = models.CharField(max_length=100)
    art_link = models.CharField(max_length=500)
    style = models.ForeignKey('styles', on_delete=models.CASCADE, related_name='styles_names')

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title
