# Generated by Django 3.2.4 on 2021-06-10 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authServer', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Useraccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('login', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=50)),
                ('admin', models.BooleanField()),
                ('make_admin', models.BooleanField()),
            ],
        ),
    ]
