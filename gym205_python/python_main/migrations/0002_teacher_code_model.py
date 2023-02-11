# Generated by Django 4.0.3 on 2023-01-18 19:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('python_main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='teacher_code_model',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('teacher_code_name', models.TextField(verbose_name='сюда название кода - для чего')),
                ('teacher_code_line', models.TextField(verbose_name='сюда вставляется код')),
                ('status', models.BooleanField(default=False, verbose_name='активирован?')),
            ],
            options={
                'verbose_name': 'Учительский код для регистрации',
                'verbose_name_plural': 'Учительский код для регистрации',
            },
        ),
    ]