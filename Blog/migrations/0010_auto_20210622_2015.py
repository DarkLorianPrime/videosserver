# Generated by Django 3.2.4 on 2021-06-22 16:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Blog', '0009_auto_20210621_1121'),
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
    ]