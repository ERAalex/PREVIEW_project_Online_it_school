# Generated by Django 4.0.3 on 2023-01-29 07:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts_cabinet', '0003_student_model'),
    ]

    operations = [
        migrations.AddField(
            model_name='student_model',
            name='user_st_login',
            field=models.CharField(max_length=200, null=True, verbose_name='имя ученика'),
        ),
    ]
