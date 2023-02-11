from django.contrib import admin
from .models import student_model, student_grades


@admin.register(student_model)
class student_mainAdmin(admin.ModelAdmin):
    list_display = ['user_username', 'user_real_name', 'class_grade', 'show_item']

@admin.register(student_grades)
class student_gradesAdmin(admin.ModelAdmin):
    list_display = ['grade_class']
