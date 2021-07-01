from django.contrib.auth.models import User
from django.db import models


class cookie_saves(models.Model):
    cookie_user_data = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cookie_user')
    cookie_user_token = models.CharField(max_length=100)

    def __str__(self):
        return self.cookie_user_data


class Role_List(models.Model):
    name = models.CharField(max_length=255)


class Role(models.Model):
    name = models.ForeignKey(Role_List, on_delete=models.CASCADE, related_name='Name_Role')
    users = models.ForeignKey(User, on_delete=models.CASCADE, related_name='User_Role_Name')

    def __str__(self):
        return str(self.users)


class Recent_res(models.Model):
    request_token = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="User_token_recent")

    def __str__(self):
        return str(self.request_token)
# Create your models here.
