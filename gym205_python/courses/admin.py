from django.contrib import admin
from .models import course_python_model, course_html_model, course_multimedia_model, homework_python, homework_html, homework_multimedia


@admin.register(course_python_model)
class course_python_model_mainAdmin(admin.ModelAdmin):
    list_display = ['lesson_name', 'lesson_number']

@admin.register(course_html_model)
class course_html_model_mainAdmin(admin.ModelAdmin):
    list_display = ['lesson_name', 'lesson_number']

@admin.register(course_multimedia_model)
class course_multimedia_model_mainAdmin(admin.ModelAdmin):
    list_display = ['lesson_name', 'lesson_number']

@admin.register(homework_python)
class homework_python_mainAdmin(admin.ModelAdmin):
    list_display = ['name_lesson', 'real_name', 'note_puntos', 'show_item', 'date_done']

@admin.register(homework_html)
class homework_html_mainAdmin(admin.ModelAdmin):
    list_display = ['name_lesson', 'real_name', 'note_puntos', 'show_item', 'date_done']

@admin.register(homework_multimedia)
class homework_multimedia_mainAdmin(admin.ModelAdmin):
    list_display = ['name_lesson', 'real_name', 'note_puntos', 'show_item', 'date_done']