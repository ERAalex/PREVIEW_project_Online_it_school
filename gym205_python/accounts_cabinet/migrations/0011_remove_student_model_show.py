# Generated by Django 4.0.3 on 2023-01-29 13:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts_cabinet', '0010_alter_student_model_show'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student_model',
            name='show',
        ),
    ]