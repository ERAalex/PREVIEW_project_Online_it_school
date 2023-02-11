from django.db import models
from django.contrib.auth.models import User

from requests import request
from django.core.exceptions import ValidationError
import os

# контроль загружаемого файла
def file_size(value):
    limit = 2 * 1024 * 1024
    if value.size > limit:
        raise ValidationError('File too large. Size should not exceed 2 MiB.')

# работает вариант 2
class Document(models.Model):
    docfile = models.FileField(upload_to='students_files/', validators=[file_size])


class student_grades(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    grade_class = models.CharField('Класс', max_length=200, null=True)

    def __str__(self):
        return self.grade_class

    class Meta:
        verbose_name = 'Все доступные классы'
        verbose_name_plural = 'Все доступные классы'



class student_model(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    user_username = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    user_name = models.CharField('логин ученика', max_length=200, null=True)
    user_real_name = models.CharField('Имя и фамилия ученика', max_length=200, null=True)
    class_grade = models.CharField('Номер класса с буквой, слитно. Например - 5в. Буква - русская', max_length=20, null=True)
    class_grade_true = models.ForeignKey(student_grades, on_delete=models.SET_NULL, null=True)
    about_self = models.CharField('о себе', max_length=200, null=True)
    show_item = models.CharField('показать? yes / no', max_length=200, null=True)

    def __str__(self):
        return self.class_grade

    class Meta:
        verbose_name = 'Личные данные ученика - о себе'
        verbose_name_plural = 'Личные данные ученика - о себе'








