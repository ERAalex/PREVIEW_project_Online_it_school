


def save_homework(request):
    today = date.today()
    date_now = today.strftime("%B %d, %Y")

    user_id = request.user.id
    result_login = request.user.username

    # загрузка файла на сервер вариант 2 работает
    if request.method == 'POST':
        form = Homework_pythonForm(request.POST, request.FILES)
        if form.is_valid():

            # проверяем сколько уже файлов у человека в папке
            dirname = f'media/{result_login}/'
            all_files = os.listdir(dirname)

            if len(all_files) >= 10:
                messages.success(request, 'Файлы НЕ ЗАГРУЖЕНЫ. У Вас уже исчерпан лимит, УДАЛИТЕ старые файлы.')
                return redirect('personal_account')

            else:
                # на самом деле тут в переменной не название урока а его id номер
                name_id_lesson = request.POST['name_lesson']

                # достаем сущность юзера и python курса, нам они нужна тк именно ее мы должны передать в поле ForeignKey
                user = User.objects.get(id=user_id)
                name_lesson_instance = course_python_model.objects.get(id=name_id_lesson)


                # Достаем информацию из редакитруемого профиля, чтобы не заставлять заполнять
                personal_data_name = student_model.objects.filter(user_username=user_id)
                real_name = ''
                real_class = ''
                for item in personal_data_name:
                    real_name = item.user_real_name
                    real_class = item.class_grade

                # проверяем есть ли уже запись сданного дз по конкретному урок
                check_instance = homework_python.objects.filter(user_username=user_id, name_lesson=name_id_lesson)



                # проверяем есть ли такой логин и данные под него, если нет. создаем
                if len(check_instance) == 0:

                    # работает сейв четко в папку, которую хотим, внутри media/{result_login}
                    myfile = request.FILES['file_lesson']


                    # проверяем, если у нас есть файл с таким именем в папке, то мы его удаляем, чтобы записать новый
                    dirname = f'media/{result_login}/'
                    all_files = os.listdir(dirname)
                    for item in all_files:
                        if item == myfile.name:
                            os.remove(f'media/{result_login}/{item}')


                    new_instance = homework_python.objects.create(
                        user_username=user,
                        name_lesson=name_lesson_instance,
                        real_name=real_name,
                        user_login=result_login,
                        class_grade=real_class,
                        note_puntos='не проверено',
                        show_item='да',
                        file_lesson=request.FILES['file_lesson']

                    )

                    messages.success(request, 'Данные успешно сохранены')
                    return redirect('personal_account')

                # если такой человек есть, просто обновляем данные
                else:
                    check_resut_note = ''
                    for item in check_instance:
                        check_resut_note = item.note_puntos

                    if check_resut_note == 'не проверено' or  check_resut_note == 'не зачет' or  check_resut_note == '2':

                        # работает сейв четко в папку, которую хотим, внутри media/{result_login}
                        myfile = request.FILES['file_lesson']

                        # проверяем, если у нас есть файл с таким именем в папке, то мы его удаляем, чтобы записать новый
                        dirname = f'media/{result_login}/'
                        all_files = os.listdir(dirname)
                        for item in all_files:
                            if item == myfile.name:
                                os.remove(f'media/{result_login}/{item}')

                        fs = FileSystemStorage(location=f'media/{result_login}/')
                        # сохраняем как имя - номер статьи урока, потом логин, потом уже имя файла
                        filename = fs.save(myfile.name, myfile)

                        change_instance = homework_python.objects.filter(user_username=user, name_lesson=name_lesson_instance).update(
                            user_username=user,
                            name_lesson=name_lesson_instance,
                            real_name=real_name,
                            user_login=result_login,
                            class_grade=real_class,
                            note_puntos='не проверено',
                            show_item='да',
                            file_lesson=request.FILES['file_lesson']
                        )

                        messages.success(request, 'Данные успешно сохранены')
                        return redirect('personal_account')

                    else:
                        messages.success(request, 'Ваша работа уже была проверена, нельзя поменять')
                        return redirect('personal_account')

    else:
        form = Homework_pythonForm

    return render(request, 'account_cabinet/account_homework_student.html',
                  {'date_now': date_now, 'result_login': result_login, 'form': form, })





# REG  RU


def save_homework(request):
    today = date.today()
    date_now = today.strftime("%B %d, %Y")

    user_id = request.user.id
    result_login = request.user.username

    # загрузка файла на сервер вариант 2 работает
    if request.method == 'POST':
        form = Homework_pythonForm(request.POST, request.FILES)
        if form.is_valid():

            try:

                # проверяем сколько уже файлов у человека в папке
                dirname = f'gym205_python/media/{result_login}/'
                all_files = os.listdir(dirname)

                if len(all_files) >= 10:
                    messages.success(request, 'Файлы НЕ ЗАГРУЖЕНЫ. У Вас уже исчерпан лимит, УДАЛИТЕ старые файлы.')

                    return redirect('personal_account')

                else:
                    # на самом деле тут в переменной не название урока а его id номер
                    name_id_lesson = request.POST['name_lesson']

                    # достаем сущность юзера и python курса, нам они нужна тк именно ее мы должны передать в поле ForeignKey
                    user = User.objects.get(id=user_id)
                    name_lesson_instance = course_python_model.objects.get(id=name_id_lesson)

                    # Достаем информацию из редакитруемого профиля, чтобы не заставлять заполнять
                    personal_data_name = student_model.objects.filter(user_username=user_id)
                    real_name = ''
                    real_class = ''
                    for item in personal_data_name:
                        real_name = item.user_real_name
                        real_class = item.class_grade

                    # проверяем есть ли уже запись сданного дз по конкретному урок
                    check_instance = homework_python.objects.filter(user_username=user_id, name_lesson=name_id_lesson)

                    # проверяем есть ли такой логин и данные под него, если нет. создаем
                    if len(check_instance) == 0:

                        # работает сейв четко в папку, которую хотим, внутри media/{result_login}
                        myfile = request.FILES['file_lesson']

                        # проверяем, если у нас есть файл с таким именем в папке, то мы его удаляем, чтобы записать новый
                        dirname = f'gym205_python/media/{result_login}/'

                        all_files = os.listdir(dirname)

                        for item in all_files:
                            if item == (str(name_lesson_instance.id) + '_' + f'{result_login}' + '_' + myfile.name):
                                os.remove(f'gym205_python/media/{result_login}/{item}')

                        new_instance = homework_python.objects.create(
                            user_username=user,
                            name_lesson=name_lesson_instance,
                            real_name=real_name,
                            user_login=result_login,
                            class_grade=real_class,
                            note_puntos='не проверено',
                            show_item='да',
                            file_lesson=request.FILES['file_lesson']

                        )

                        messages.success(request, 'Данные успешно сохранены')
                        return redirect('personal_account')

                    # если такой человек есть, просто обновляем данные
                    else:

                        check_resut_note = ''
                        for item in check_instance:
                            check_resut_note = item.note_puntos

                        if check_resut_note == 'не проверено' or check_resut_note == 'не зачет' or check_resut_note == '2':

                            # работает сейв четко в папку, которую хотим, внутри media/{result_login}
                            myfile = request.FILES['file_lesson']

                            # проверяем, если у нас есть файл с таким именем в папке, то мы его удаляем, чтобы записать новый
                            dirname = f'gym205_python/media/{result_login}/'
                            all_files = os.listdir(dirname)
                            for item in all_files:
                                if item == myfile.name:
                                    os.remove(f'gym205_python/media/{result_login}/{item}')

                            fs = FileSystemStorage(location=f'gym205_python/media/{result_login}/')
                            # сохраняем как имя - номер статьи урока, потом логин, потом уже имя файла
                            filename = fs.save(myfile.name, myfile)

                            change_instance = homework_python.objects.filter(user_username=user,
                                                                             name_lesson=name_lesson_instance).update(
                                user_username=user,
                                name_lesson=name_lesson_instance,
                                real_name=real_name,
                                user_login=result_login,
                                class_grade=real_class,
                                note_puntos='не проверено',
                                show_item='да',
                                file_lesson=request.FILES['file_lesson']
                            )

                            messages.success(request, 'Данные успешно сохранены')
                            return redirect('personal_account')

                        else:
                            messages.success(request, 'Ваша работа уже была проверена, ее нельзя исправить')
                            return redirect('personal_account')


            except:

                messages.success(request, f'ошибка на {yes}')
                return redirect('personal_account')

    else:
        form = Homework_pythonForm

    return render(request, 'account_cabinet/account_homework_student.html',
                  {'date_now': date_now, 'result_login': result_login, 'form': form, })

