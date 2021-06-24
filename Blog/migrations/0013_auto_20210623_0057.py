# Generated by Django 3.2.4 on 2021-06-22 20:57

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('Blog', '0012_auto_20210622_2015'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='actors',
            field=models.ManyToManyField(to='Blog.Actors'),
        ),
        migrations.AlterField(
            model_name='post',
            name='producer',
            field=models.ManyToManyField(to='Blog.Prod'),
        ),
        migrations.AlterField(
            model_name='post',
            name='publish',
            field=models.DateTimeField(default=datetime.datetime(2021, 6, 22, 20, 57, 39, 7427, tzinfo=utc)),
        ),
    ]
