# Generated by Django 3.2.4 on 2021-06-22 16:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authServer', '0021_auto_20210622_1958'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cookie_saves',
            old_name='cookie_user',
            new_name='cookie_user_data',
        ),
    ]
