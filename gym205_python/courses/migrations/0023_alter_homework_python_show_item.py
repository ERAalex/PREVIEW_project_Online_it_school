# Generated by Django 4.0.3 on 2023-02-07 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0022_alter_homework_python_show_item'),
    ]

    operations = [
        migrations.AlterField(
            model_name='homework_python',
            name='show_item',
            field=models.CharField(max_length=20, null=True, verbose_name='Показывать задание?'),
        ),
    ]
