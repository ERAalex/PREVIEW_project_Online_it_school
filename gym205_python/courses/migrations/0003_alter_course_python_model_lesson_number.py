# Generated by Django 4.0.3 on 2023-01-27 19:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0002_homework_done'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course_python_model',
            name='lesson_number',
            field=models.IntegerField(null=True),
        ),
    ]
