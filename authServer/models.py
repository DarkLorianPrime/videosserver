from django.contrib.auth.models import User
from django.db import models


class cookie_saves(models.Model):
    cookie_user_id = models.CharField(max_length=100)
    cookie_user_token = models.CharField(max_length=100)

    def __str__(self):
        return self.cookie_user_id


class not_Admin(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Admin(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
# Create your models here.
