# Generated by Django 5.1 on 2024-08-22 08:11

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Leaderboards', '0005_rename_points_pointtable_nafl_points_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='pointtable',
            unique_together={('user', 'date')},
        ),
    ]
