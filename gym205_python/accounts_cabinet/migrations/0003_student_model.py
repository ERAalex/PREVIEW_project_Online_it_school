# Generated by Django 4.0.3 on 2023-01-29 07:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts_cabinet', '0002_alter_document_docfile'),
    ]

    operations = [
        migrations.CreateModel(
            name='student_model',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('class_grade', models.CharField(max_length=20, null=True, verbose_name='номер класса с буквой, слитно. Например - 5в')),
                ('about_self', models.CharField(max_length=200, null=True, verbose_name='название урока')),
                ('show', models.BooleanField(default=True, verbose_name='показать статью?')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Личные данные ученика - о себе',
                'verbose_name_plural': 'Личные данные ученика - о себе',
            },
        ),
    ]