# Generated by Django 3.2.4 on 2021-06-17 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Blog', '0007_rating'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='actors',
        ),
        migrations.AddField(
            model_name='post',
            name='actors',
            field=models.ManyToManyField(to='Blog.Actors'),
        ),
        migrations.RemoveField(
            model_name='post',
            name='producer',
        ),
        migrations.AddField(
            model_name='post',
            name='producer',
            field=models.ManyToManyField(to='Blog.Prod'),
        ),
    ]
