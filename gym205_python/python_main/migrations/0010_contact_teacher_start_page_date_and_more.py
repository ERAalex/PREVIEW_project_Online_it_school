# Generated by Django 4.0.3 on 2023-01-19 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('python_main', '0009_alter_contact_teacher_start_page_text_contact_start'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact_teacher_start_page',
            name='date',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='contact_teacher_start_page',
            name='theme_contact_start',
            field=models.TextField(null=True, verbose_name='тема'),
        ),
    ]
