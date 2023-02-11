from django.db import models
from django.contrib.auth.models import User
import os
from django.core.exceptions import ValidationError
from django.utils import timezone


class course_python_model(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    block_lesson = models.CharField('блок заданий - введение и т.д.', max_length=200, null=True)
    lesson_number = models.IntegerField(null=True)
    lesson_name = models.CharField('название урока', max_length=200, null=True)
    theory = models.TextField('сама теория', max_length=6000, null=True)
    tasks = models.TextField('задания', max_length=6000, null=True)

    show = models.BooleanField('показать статью?', default=False)

    def __str__(self):
        return self.lesson_name

    class Meta:
        verbose_name = 'Курс по Python'
        verbose_name_plural = 'Курс по Python'


class course_html_model(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    block_lesson = models.CharField('блок заданий - введение и т.д.', max_length=200, null=True)
    lesson_number = models.IntegerField(null=True)
    lesson_name = models.CharField('название урока', max_length=200, null=True)
    theory = models.TextField('сама теория', max_length=6000, null=True)
    tasks = models.TextField('задания', max_length=6000, null=True)

    show = models.BooleanField('показать статью?', default=False)

    def __str__(self):
        return self.lesson_name

    class Meta:
        verbose_name = 'Курс по HTML'
        verbose_name_plural = 'Курс по HTML'



class course_multimedia_model(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    block_lesson = models.CharField('блок заданий - введение и т.д.', max_length=200, null=True)
    lesson_number = models.IntegerField(null=True)
    lesson_name = models.CharField('название урока', max_length=200, null=True)
    theory = models.TextField('сама теория', max_length=8000, null=True)
    tasks = models.TextField('задания', max_length=8000, null=True)

    show = models.BooleanField('показать статью?', default=False)

    def __str__(self):
        return self.lesson_name

    class Meta:
        verbose_name = 'Курс по Multimedia'
        verbose_name_plural = 'Курс по Multimedia'



# БЛОК ПО ОЦЕНКАМ
# проверяем размер
def file_size(value):
    limit = 2 * 1024 * 1024
    if value.size > limit:
        raise ValidationError('Загрузка отменена - СЛИШКОМ БОЛЬШОЙ ФАЙЛ. Допустимый размер не более 2МБ')

# сохраняем новый путь для файла, достаем имя юзера через поле user_username в таблице.
def get_upload_path(instance, filename):
    return "{username}/{file}".format(username=instance.user_username.username, file=filename)

# нет в Myscql постановки время, приходится таким костылем добавлять автоматическое время
class AutoDateTimeField(models.DateTimeField):
    def pre_save(self, model_instance, add):
        return timezone.now()



class homework_python(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    user_username = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name_lesson = models.ForeignKey(course_python_model, on_delete=models.CASCADE, null=True)
    real_name = models.CharField('Фамилия', max_length=200, null=True)
    user_login = models.CharField('Логин', max_length=200, null=True)
    class_grade = models.CharField('Номер класса с буквой', max_length=20, null=True)
    note_puntos = models.CharField('Оценка', max_length=20, null=True)
    date_done = models.DateField('Дата', default=timezone.now)
    show_item = models.CharField('Показывать задание?', max_length=20, null=True)
    file_lesson = models.FileField(upload_to=get_upload_path, validators=[file_size])

    def __str__(self):
        return self.class_grade

    class Meta:
        verbose_name = 'Выполненные задания - Python'
        verbose_name_plural = 'Выполненные задания - Python'


class homework_html(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    user_username = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name_lesson = models.ForeignKey(course_html_model, on_delete=models.CASCADE, null=True)
    real_name = models.CharField('Фамилия', max_length=200, null=True)
    user_login = models.CharField('Логин', max_length=200, null=True)
    class_grade = models.CharField('Номер класса с буквой', max_length=20, null=True)
    note_puntos = models.CharField('Оценка', max_length=20, null=True)
    date_done = models.DateField('Дата', default=timezone.now)
    show_item = models.CharField('Показывать задание?', max_length=20, null=True)
    file_lesson = models.FileField(upload_to=get_upload_path, validators=[file_size])

    def __str__(self):
        return self.class_grade

    class Meta:
        verbose_name = 'Выполненные задания - HTML'
        verbose_name_plural = 'Выполненные задания - HTML'



class homework_multimedia(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    user_username = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name_lesson = models.ForeignKey(course_multimedia_model, on_delete=models.CASCADE, null=True)
    real_name = models.CharField('Фамилия', max_length=200, null=True)
    user_login = models.CharField('Логин', max_length=200, null=True)
    class_grade = models.CharField('Номер класса с буквой', max_length=20, null=True)
    note_puntos = models.CharField('Оценка', max_length=20, null=True)
    date_done = models.DateField('Дата', default=timezone.now)
    show_item = models.CharField('Показывать задание?', max_length=20, null=True)
    file_lesson = models.FileField(upload_to=get_upload_path, validators=[file_size])

    def __str__(self):
        return self.class_grade

    class Meta:
        verbose_name = 'Выполненные задания - Multimedia'
        verbose_name_plural = 'Выполненные задания - Multimedia'

