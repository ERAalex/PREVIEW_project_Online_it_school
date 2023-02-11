from django.urls import path
from django.urls import include, re_path
from django.conf import settings
from django.contrib.auth.views import LogoutView
from . import views



urlpatterns = [
    # личный кабинет
    path('personal_account', views.personal_account, name='personal_account'),

    # обновть свои персональные данные - класс и тд
    path('change_data', views.change_data_student, name='change_data'),

    # удалить файлы
    path('delete_files', views.delete_files, name='delete_files'),

    # готовим ссылку в html будем передавать параметры и потом их в вьюшку
    path('delete_simple/<str:user_folder>/<str:user_file>/', views.delete_simple_admin, name='delete_simple_admin'),

    path('find_student', views.find_student, name='find_student'),

    path('no_post/<str:login_user>', views.find_student_no_post, name='find_student_no_post'),

    path('find_student_class', views.find_student_class, name='find_student_class'),

    path('admin_account', views.admin_accounts_view, name='admin_acc'),

    # ставим домашнее задание не активным PYTHON
    path('change_show/<int:id>/<str:user_name>', views.dont_show_homework_python, name='change_show'),

    # ставим домашнее задание не активным HTML
    path('change_show_html/<int:id>/<str:user_name>', views.dont_show_homework_html, name='change_show_html'),

    # готовим ссылку в html будем передавать параметры и потом их в вьюшку
    path('download/<str:user_folder>/<str:user_file>/', views.download_file, name='download_file'),

    # изменить статус проверки домашнего задания Python
    path('new_note/<str:id>', views.put_note, name='new_note'),

    # изменить статус проверки домашнего задания HTML
    path('html_new_note/<str:id>', views.put_note_html, name='html_new_note'),
]