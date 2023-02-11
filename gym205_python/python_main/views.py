from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.core.mail import send_mail
from django.contrib import messages
from .forms import LoginForm, UserRegistrationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test

from django.contrib.auth.models import User
from .email_code import email_check
from django.core.mail import send_mail
from datetime import date
from pathlib import Path

import random

import mysql.connector
from time import sleep
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth



con = mysql.connector.connect(user='',
                              password='',
                              host='',
                              database='')

mycursor = con.cursor()




def generate_code():
    random.seed()
    return str(random.randint(10000, 99999))



def start_index(request):
    # Форма регистрации пользователя
    if request.method == 'POST':
        try:
            user_form = UserRegistrationForm(request.POST)
            if user_form.is_valid():
                # Create a new user object but avoid saving it yet
                new_user = user_form.save(commit=False)
                # Set the chosen password
                new_user.set_password(user_form.cleaned_data['password'])
                # Save the User object
                new_user.save()

                # достаем из одобренной формы данные через cleaned_data
                email_search = user_form.cleaned_data['email']
                name_search = user_form.cleaned_data['first_name']

                #ищем юзера по таблице БД нам нужен его ID
                query = ("SELECT id FROM auth_user WHERE email=%s")
                mycursor.execute(query, (email_search,))
                result_list = mycursor.fetchall()
                result_id = ''
                for x in result_list:
                    for item in x:
                        result_id = item


                check_code = generate_code()

                #сохраняем нашего юзера в БД verification
                insert_data_code = """
                    INSERT INTO python_main_user_verification_code (user_id_id, verification_code, status, email)
                    VALUES ( %s, %s, %s, %s ) """
                data_records = [f'{result_id}', f'{check_code}', 0, f'{email_search}']
                with con.cursor() as cursor:
                    cursor.execute(insert_data_code, data_records)
                    con.commit()

                verification_name_field = 'код для Верификации'
                #ищем код учителя для регистрации, чтобы отправить сразу на почту
                query = ("SELECT teacher_code_line FROM python_main_teacher_code_model WHERE teacher_code_name=%s")
                mycursor.execute(query, (verification_name_field,))
                result_list = mycursor.fetchall()
                teacher_code_result = ''
                for x in result_list:
                    for item in x:
                        teacher_code_result = item

                # создаем рандомный пароль, его сохраним в базу и отправим на почту. потом человек открывает почту
                # и там будет не только пароль, но и ссылка, он переходит. вбивает свою почту и пароль и если все хорошо
                # (проверка по базе данных), то его аккаунт становится активным.
                mail = send_mail(f'{check_code}', f'Уважаемый ---- {name_search} ---- Вам нужно пройти '
                                                  f'по ссылке http://127.0.0.1:8000/verification_ind и ввести:\n\n'
                                                  f'свою почту: {email_search} \n\n'
                                                  f'код верификации: {check_code} \n\n'
                                                  f'код учителя: {teacher_code_result} \n\n', 'erapyth@gmail.com',
                                 [f'{email_search}'], fail_silently=False)


                messages.success(request, 'Аккаунт создан, проверьте почту для завершения регистрации')
                return render(request, 'python_main/start_index.html', {'new_user': new_user})

        except:
            messages.error(request, 'Вы ввели некорректные данные. Почта уже используется')
            return render(request, 'python_main/start_index.html')

    else:
        user_form = UserRegistrationForm()

    return render(request, 'python_main/start_index.html', {'user_form': user_form })



###########______Контакт с разработчиками с главной страницы______###########
def contact_start(request):
    if request.method == 'POST':
        contact_email = request.POST['contact_mail']
        contact_message = request.POST['contact_message']

        time_date = date.today()


        if '@' in contact_email:

            # ищем юзера по таблице БД по его почте
            query = ("SELECT username FROM auth_user WHERE email=%s")
            mycursor.execute(query, (contact_email,))
            result_list = mycursor.fetchall()
            result_username = ''
            for x in result_list:
                for item in x:
                    result_username = item

            if result_username == '':
                messages.error(request, 'К сожалению мы не можем Вам помочь, обратитесь напрямую по почте,'
                                        'указанной в пункте контакты')
                return render(request, 'python_main/start_index.html')

            else:
                insert_data_code = """
                    INSERT INTO python_main_contact_teacher_start_page (email_contact_start, text_contact_start, date)
                    VALUES ( %s, %s, %s ) """
                data_records = [f'{contact_email}', f'{contact_message}', f'{time_date}']
                with con.cursor() as cursor:
                    cursor.execute(insert_data_code, data_records)
                    con.commit()
                messages.success(request, 'Обращение к администраторам сайта отправлено')
        else:
            messages.error(request, 'Ошибка, сообщение не отправлено, проверьте данные')
    return render(request, 'python_main/start_index.html')




# Блок страницы с регистрацией пользователя
def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('start_index')
        else:
            messages.info(request, 'Неправильный ввод Username или Password')
            return redirect('login_user')
    else:
        return render(request, 'python_main/registration/login_index.html')



# Блок запроса нового пароля
def restart_pass(request):
    if request.method == 'POST':
        useremail = request.POST['useremail']

        try:
            # ищем юзера по таблице БД по его почте
            query = ("SELECT username FROM auth_user WHERE email=%s")
            mycursor.execute(query, (useremail,))
            result_list = mycursor.fetchall()
            result_username = ''
            for x in result_list:
                for item in x:
                    result_username = item

            if result_username == '':
                messages.error(request, 'Такая почта не найдена')
                return render(request, 'python_main/registration/restart_password.html')

            else:
                #создаем новый код
                check_code = generate_code()

                #сохраняем новый код в базе нашего юзера
                update_data_code = f"""
                    UPDATE python_main_user_verification_code
                    SET verification_code=%s
                    WHERE email=%s """
                data_records = [f'{check_code}', f'{useremail}']
                with con.cursor() as cursor:
                    cursor.execute(update_data_code, data_records)
                    con.commit()


                mail = send_mail(f'{check_code}',f'ЗАПРОС НА СБРОС ПАРОЛЯ. Уважаемый пользователь,'
                                                 f'\n\nВаш логин: {result_username}, запомните его.\n\n'
                                 f'Ваш код для реактивации аккаунта: {check_code} \n\n'
                                 f'Перейдите по ссылке и введите данные: http://127.0.0.1:8000/reset_passw', 'erapyth@gmail.com',
                                 [f'{useremail}'], fail_silently=False)

                messages.success(request, 'На Вашу почту отправлены данные для восстановления пароля')
                return render(request, 'python_main/start_index.html')
        except:
            messages.success(request, 'Не удалось сбросить пароль, проверьте правильность заполнения почты или обратитесь'
                                      'к администраторам')
            return render(request, 'python_main/registration/restart_password.html')
    return render(request, 'python_main/registration/restart_password.html')



####  THE REST OF THE CODE IS AVAILABLE TO EMPLOYERS UPON REQUEST. CONTACT ME VIA TELEGRAM, MAIL ####
################################# MORE THEN 150+ LINES OF CODE ######################################
###################################### ESPINOSA ROZOV ALEX ##########################################