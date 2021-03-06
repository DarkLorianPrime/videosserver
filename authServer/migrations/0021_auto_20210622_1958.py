# Generated by Django 3.2.4 on 2021-06-22 15:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('authServer', '0020_role'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Admin',
        ),
        migrations.DeleteModel(
            name='Moderator',
        ),
        migrations.RemoveField(
            model_name='cookie_saves',
            name='cookie_user_id',
        ),
        migrations.AddField(
            model_name='cookie_saves',
            name='cookie_user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='cookie_user', to='auth.user'),
            preserve_default=False,
        ),
    ]
