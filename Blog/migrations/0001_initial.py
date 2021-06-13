# Generated by Django 3.2.4 on 2021-06-11 13:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='actors',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='prod',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('slug', models.SlugField(max_length=250, unique_for_date='publish')),
                ('description', models.TextField()),
                ('publish', models.DateTimeField(default=django.utils.timezone.now)),
                ('art_link', models.CharField(max_length=500)),
                ('actors', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='actor', to='Blog.actors')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='film_post', to=settings.AUTH_USER_MODEL)),
                ('producer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prod', to='Blog.prod')),
            ],
            options={
                'ordering': ('-publish',),
            },
        ),
    ]
