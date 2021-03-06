# Generated by Django 3.2.4 on 2021-06-21 07:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Blog', '0008_auto_20210617_1927'),
    ]

    operations = [
        migrations.CreateModel(
            name='Entire_rating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('entire_stars', models.IntegerField()),
            ],
        ),
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
            name='title',
            field=models.CharField(default='None', max_length=50),
        ),
    ]
