# Generated by Django 3.2.4 on 2021-06-22 22:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authServer', '0023_auto_20210622_2357'),
    ]

    operations = [
        migrations.RenameField(
            model_name='role',
            old_name='Name',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='role',
            old_name='Users',
            new_name='users',
        ),
    ]