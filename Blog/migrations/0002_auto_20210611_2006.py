# Generated by Django 3.2.4 on 2021-06-11 16:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Blog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='styles',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('style', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='style',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='styles_names', to='Blog.styles'),
            preserve_default=False,
        ),
    ]
