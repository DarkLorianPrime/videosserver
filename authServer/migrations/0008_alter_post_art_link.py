# Generated by Django 3.2.4 on 2021-06-10 16:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authServer', '0007_auto_20210610_2026'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='art_link',
            field=models.CharField(max_length=500),
        ),
    ]
