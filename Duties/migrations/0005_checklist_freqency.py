# Generated by Django 5.1 on 2024-08-19 07:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Duties', '0004_task_for_female_task_for_unmarried'),
    ]

    operations = [
        migrations.AddField(
            model_name='checklist',
            name='freqency',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
    ]
