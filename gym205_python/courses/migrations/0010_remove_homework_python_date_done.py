# Generated by Django 4.0.3 on 2023-01-31 17:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0009_homework_python_date_done'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='homework_python',
            name='date_done',
        ),
    ]
