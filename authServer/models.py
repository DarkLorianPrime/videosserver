from django.contrib.auth.models import User
from django.db import models


class cookie_saves(models.Model):
    cookie_user_id = models.CharField(max_length=100)
    cookie_user_token = models.CharField(max_length=100)

    def __str__(self):
        return self.cookie_user_id


class Role(models.Model):
    name = models.CharField(max_length=255)
    Users = models.ForeignKey(User, on_delete=models.CASCADE, related_name='styles_names')
    is_Role = models.BooleanField()

    def __str__(self):
        return str(self.Users)


class Moderator(models.Model):
    name = models.CharField(max_length=255)
    is_moder = models.BooleanField()

    def __str__(self):
        return self.name


class Admin(models.Model):
    name = models.CharField(max_length=255)
    is_admin = models.BooleanField()

    def __str__(self):
        return self.name
# Create your models here.
