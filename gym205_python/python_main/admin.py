from django.contrib import admin
from python_main.models import user_verification_code, teacher_code_model, contact_teacher_start_page


@admin.register(user_verification_code)
class user_verification_code_mainAdmin(admin.ModelAdmin):
    list_display = ['email', 'verification_code']

@admin.register(teacher_code_model)
class teacher_code_model_mainAdmin(admin.ModelAdmin):
    list_display = ['teacher_code_name', 'teacher_code_line']


@admin.register(contact_teacher_start_page)
class contact_teacher_start_page_mainAdmin(admin.ModelAdmin):
    list_display = ['email_contact_start', 'date']