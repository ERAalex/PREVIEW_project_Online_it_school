import mimetypes

from django.http import Http404, HttpResponseRedirect, HttpResponse
from .forms import *
from courses.models import homework_python, homework_html, homework_multimedia

from django.contrib import messages
from datetime import date

from .models import *
import os
import shutil

import mysql.connector
from time import sleep
from django.shortcuts import render, redirect


import os
import mimetypes

from wsgiref.util import FileWrapper
from django.http import StreamingHttpResponse



con = mysql.connector.connect(user='',
                              password='',
                              host='',
                              database='')

mycursor = con.cursor()


def check_user_able_to_see_page(*groups):

    def decorator(function):
        def wrapper(request, *args, **kwargs):
            if request.user.groups.filter(name__in=groups).exists():
                return function(request, *args, **kwargs)
            else:
                not_registr = 'Вы не можете посетить сайт, без полной регистрации!'
                return render(request, 'python_main/start_index.html', {'not_registr': not_registr})

        return wrapper

    return decorator




@check_user_able_to_see_page('admin')
def admin_accounts_view(request):
    array = os.listdir('media/')  # получаем список папок

    # сохраняем в словарь как ключ имя студента и как значение список файлов
    all_files = {}
    for name_dirr in array:
        path = f'media/{name_dirr}'
        path_files = os.listdir(path)
        all_files[name_dirr] = path_files


    return render(request, 'account_cabinet/account_cab_admin.html', {'all_files': all_files})



@check_user_able_to_see_page('students')
def personal_account(request):
    today = date.today()
    date_now = today.strftime("%B %d, %Y")
    user_id = request.user.id
    user_login = request.user.username

    # ссылка на аватар
    href_image = f'accounts_cabinet/files_students/{user_login}/avatar.jpg'

    # личные данные - класс и тд
    personal_data = student_model.objects.filter(user_name=user_login)
    homeworks_pyth = homework_python.objects.filter(user_login=user_login, show_item='да')
    homeworks_html = homework_html.objects.filter(user_login=user_login, show_item='да')
    homeworks_multimedia = homework_multimedia.objects.filter(user_login=user_login, show_item='да')


    # тут мы поулчаем кортеж с 2 данными требуемыми
    query = ("SELECT email, username FROM auth_user WHERE id=%s")
    mycursor.execute(query, (user_id,))
    result_list = mycursor.fetchall()
    result_email = ''
    result_login = ''
    for x in result_list:
        result_email = x[0]
        result_login = x[1]

    if result_email == '':
        result_email = 'почта не указана'

    # получаем список всех файлов в папке ученика из media
    try:
        # dirname = f'media/{result_login}/'
        dirname = f'media/{result_login}/'
        all_files = os.listdir(dirname)
        error_files = ''
        if len(all_files) == 0:
            error_files = 'У Вас нет файлов.'
    except:
        all_files = ''
        error_files = 'Файлы не найдены, обратитесь к администратору'



    # загрузка файла на сервер вариант 2 работает
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            # проверка на количество файлов в папке
            if len(all_files) >= 10:
                messages.error(request, 'У Вас уже лимит по файлам. Удалите, и сможете загрузить новые.')
                return redirect('personal_account')
            else:
                try:
                    result = form.save()
                    # сохраняем имя файла, чтобы его найти потом
                    filename_to_find = request.FILES['docfile'].name

                    # переносим файл в папку пользователя
                    shutil.move(f'media/students_files/{filename_to_find}',
                                f'media/{result_login}/{filename_to_find}')
                    # переименовываем файл на всякий, даем в начале его id пользователя
                    os.rename(f'media/{result_login}/{filename_to_find}',
                              f'media/{result_login}/{result_login}_{filename_to_find}')

                    messages.success(request, 'Файл успешно загружен')
                    return redirect('personal_account')
                except:
                    messages.error(request, 'Файл не был загружен, возможно такой файл уже существует.')
                    return redirect('personal_account')

    else:
        form = DocumentForm


    return render(request, 'account_cabinet/account_cab.html',
                  {'date_now': date_now, 'result_email': result_email,
                   'result_login': result_login, 'all_files': all_files,
                   'error_files': error_files, 'form': form, 'personal_data': personal_data,
                   'href_image': href_image, 'homeworks_pyth': homeworks_pyth,
                   'homeworks_html': homeworks_html,
                   'homeworks_multimedia': homeworks_multimedia})




def change_data_student(request):
    today = date.today()
    date_now = today.strftime("%B %d, %Y")

    user_id = request.user.id
    result_login = request.user.username

    name_form = StudentForm(request.POST)
    if request.method == 'POST':
        if name_form.is_valid():

            class_grade_g = request.POST['class_grade_true']
            about_self_g = request.POST['about_self']
            real_name = request.POST['user_real_name']

            check_instance = student_model.objects.filter(user_name=result_login)
            # проверяем есть ли такой логин и данные под него, если нет. создаем
            if len(check_instance) == 0:
                new_instance = student_model.objects.create(
                    user_username_id=user_id,
                    user_name=result_login,
                    class_grade='запасное поле',
                    class_grade_true=class_grade_g,
                    about_self=about_self_g,
                    show_item='yes',
                    user_real_name=real_name
                )
            # если такой человек есть, просто обнволяем данные
            else:
                student_model.objects.filter(user_name=result_login).update(
                    user_username_id=user_id,
                    user_name=result_login,
                    class_grade='запасное поле',
                    class_grade_true=class_grade_g,
                    about_self=about_self_g,
                    show_item='yes',
                    user_real_name=real_name
                )

            messages.success(request, 'Данные успешно сохранены')
            return render(request, 'account_cabinet/account_data_student.html', {'name_form': name_form,
                                                                                 'date_now': date_now,
                                                                                 'result_login': result_login})

    return render(request, 'account_cabinet/account_data_student.html', {'name_form': name_form,
                                                                         'date_now': date_now,
                                                                         'result_login': result_login})





def find_student(request):
    try:
        if request.method == 'POST':
            find = request.POST['find']
            path_files = os.listdir(f'media/{find}')  # получаем список файлов

            # личные данные - класс и тд
            personal_data = student_model.objects.filter(user_name=find)
            homeworks_pyth = homework_python.objects.filter(user_login=find, show_item='да')

            # сохраняем в словарь как ключ имя студента и как значение файл
            all_files = {}
            all_files[find] = path_files


            return render(request, 'account_cabinet/account_cab_admin.html', {'all_files': all_files,
                                                                              'personal_data': personal_data,
                                                                              'homeworks_pyth': homeworks_pyth,
                                                                              })
    except:
        return render(request, 'account_cabinet/account_cab_admin.html')
    return render(request, 'account_cabinet/account_cab_admin.html')



def find_student_no_post(request, login_user=''):
    try:
        path_files = os.listdir(f'media/{login_user}')  # получаем список файлов

        # личные данные - класс и тд
        personal_data = student_model.objects.filter(user_name=login_user)
        homeworks_pyth = homework_python.objects.filter(user_login=login_user, show_item='да')
        homeworks_html = homework_html.objects.filter(user_login=login_user, show_item='да')

        # сохраняем в словарь как ключ имя студента и как значение файл
        all_files = {}
        all_files[login_user] = path_files
        return render(request, 'account_cabinet/account_cab_admin.html', {'all_files': all_files,
                                                                              'personal_data': personal_data,
                                                                              'homeworks_pyth': homeworks_pyth,
                                                                              'homeworks_html': homeworks_html,
                                                                              })
    except:
        redirect('admin_acc')
    return render(request, 'account_cabinet/account_cab_admin.html')




def find_student_class(request):
    try:
        if request.method == 'POST':
            find_class = request.POST['find_class']

            # хитрый момент, нам нужно через Foreign Key найти данные ученика. снчало пичем поле модели Foreign key
            # затем _ _ потом поле второй модели в которой будем искать соответсвие потом _ _ и слово contains (содержит)
            personal_data = student_model.objects.filter(class_grade_true__grade_class__contains=find_class)

            list_students = []
            # сохраняем в словарь реальные имена ключ - логин, чтобы потом в шаблоне перебором при совпадении
            # выводить реальные имена
            all_real_names = {}
            for item in personal_data:
                list_students.append(item.user_name)
                all_real_names[item.user_name] = item.user_real_name

            all_files = {}

            for find in list_students:
                path_files = os.listdir(f'accounts_cabinet/files_students/{find}')  # получаем список файлов

                # сохраняем в словарь как ключ имя студента и как значение файл
                all_files[find] = path_files
            return render(request, 'account_cabinet/account_cab_admin.html', {'all_files': all_files,
                                                                              'all_real_names': all_real_names})
    except:
        return render(request, 'account_cabinet/account_cab_admin.html')
    return render(request, 'account_cabinet/account_cab_admin.html')




def find_documents_students():
    array = os.listdir('media/')  # получаем список папок

    # сохраняем в словарь как ключ имя студента и как значение список файлов
    all_files = {}
    for name_dirr in array:
        path = f'media/{name_dirr}'
        path_files = os.listdir(path)
        all_files[name_dirr] = path_files
    return all_files



####  THE REST OF THE CODE IS AVAILABLE TO EMPLOYERS UPON REQUEST. CONTACT ME VIA TELEGRAM, MAIL ####
################################# MORE THEN 150+ LINES OF CODE ######################################
###################################### ESPINOSA ROZOV ALEX ##########################################