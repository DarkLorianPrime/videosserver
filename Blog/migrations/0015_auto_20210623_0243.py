# Generated by Django 3.2.4 on 2021-06-22 22:43

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Blog', '0014_auto_20210623_0240'),
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
            field=models.DateTimeField(default=datetime.datetime(2021, 6, 22, 22, 43, 45, 7056, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='rating',
            name='name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='all_rating_post', to='Blog.post'),
        ),
        migrations.AlterField(
            model_name='rating',
            name='username',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='username_rater', to=settings.AUTH_USER_MODEL),
        ),
    ]
