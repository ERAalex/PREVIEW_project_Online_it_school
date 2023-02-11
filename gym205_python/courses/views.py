from django.core.files.storage import FileSystemStorage
from django.views.generic import DetailView
from .models import *
from datetime import date
import mysql.connector
from .forms import *
from django.contrib import messages
from django.shortcuts import render, redirect
from accounts_cabinet.models import student_model

from django.contrib.auth.models import User



con = mysql.connector.connect(user='',
                              password='',
                              host='',
                              database='')
mycursor = con.cursor()



def python_course(request):
    today = date.today()
    date_now = today.strftime("%B %d, %Y")

    all_articles = course_python_model.objects.order_by('lesson_number')
    total_articles = len(all_articles)

    return render(request, 'courses/course_python.html', {'date_now': date_now, 'all_articles': all_articles,
                                                          'total_articles': total_articles})


# детальный вывод на отдельной странице статей модели
class course_python_DetailView(DetailView):
    model = course_python_model
    template_name = 'courses/course_python_detail.html'
    # определяем имя article для использования в шаблоне
    context_object_name = 'article'


    def get_context_data(self, **kwargs):
        context = super(course_python_DetailView, self).get_context_data(**kwargs)

        today = date.today()
        date_now = today.strftime("%B %d, %Y")

        context['date_now'] = date_now
        return context




def multimedia_course(request):
    today = date.today()
    date_now = today.strftime("%B %d, %Y")

    all_articles = course_multimedia_model.objects.order_by('lesson_number')
    total_articles = len(all_articles)

    return render(request, 'courses/course_multimedia.html', {'date_now': date_now, 'all_articles': all_articles,
                                                          'total_articles': total_articles})

# детальный вывод на отдельной странице статей модели
class course_multimedia_DetailView(DetailView):
    model = course_multimedia_model
    template_name = 'courses/course_multimedia_detail.html'
    # определяем имя article для использования в шаблоне
    context_object_name = 'article'

    def get_context_data(self, **kwargs):
        context = super(course_multimedia_DetailView, self).get_context_data(**kwargs)

        today = date.today()
        date_now = today.strftime("%B %d, %Y")

        context['date_now'] = date_now
        return context


def html_course(request):
    today = date.today()
    date_now = today.strftime("%B %d, %Y")

    all_articles_html = course_html_model.objects.order_by('lesson_number')
    total_articles = len(all_articles_html)

    return render(request, 'courses/course_html.html', {'date_now': date_now, 'all_articles_html': all_articles_html,
                                                        'total_articles': total_articles})


# детальный вывод на отдельной странице статей модели
class course_html_DetailView(DetailView):
    model = course_html_model
    template_name = 'courses/course_html_detail.html'
    # определяем имя article для использования в шаблоне
    context_object_name = 'article_html'


    def get_context_data(self, **kwargs):
        context = super(course_html_DetailView, self).get_context_data(**kwargs)

        today = date.today()
        date_now = today.strftime("%B %d, %Y")

        context['date_now'] = date_now
        return context



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
    else:
        form = Homework_pythonForm

    return render(request, 'account_cabinet/account_homework_student.html',
                  {'date_now': date_now, 'result_login': result_login, 'form': form, })



def delete_homework_python(request, id=''):
    result_login = request.user.username
    change_instance = homework_python.objects.filter(id=int(id, ))
    file_name = ''

    # здесь хитрый момент сам файл item.file_lesson не является строкой, а элементом, поэтому нам нужно достать имя как STR - item.file_lesson.name
    for item in change_instance:
        file_name = item.file_lesson.name

    size = len(result_login) + 1

    change_instance = homework_python.objects.filter(id=int(id, )).delete()
    messages.success(request, 'Этот урок с заданием - удален')

    try:
        path = f'media/{result_login}/{file_name[size:]}'
        os.remove(path)
        # обновляем список файлов
    except:
        messages.success(request,
                         'Этот урок с заданием - удален, НО файл не удалось удалить,\n проверьте если он остался'
                         'в папке, и удалите в ручную\n имя файла', extra_tags=file_name[size:])

    return redirect('personal_account')


def delete_homework_html(request, id=''):
    result_login = request.user.username
    change_instance = homework_html.objects.filter(id=int(id, ))
    file_name = ''

    # здесь хитрый момент сам файл item.file_lesson не является строкой, а элементом, поэтому нам нужно достать имя как STR - item.file_lesson.name
    for item in change_instance:
        file_name = item.file_lesson.name

    # нам нужно взять название файла без логина, те от знака '/'

    size = len(result_login) + 1

    change_instance = homework_html.objects.filter(id=int(id, )).delete()
    messages.success(request, 'Этот урок с заданием - удален')

    try:
        path = f'media/{result_login}/{file_name[size:]}'
        os.remove(path)
        # обновляем список файлов
    except:
        messages.success(request,
                         'Этот урок с заданием - удален, НО файл не удалось удалить,\n проверьте если он остался'
                         'в папке, и удалите в ручную\n имя файла', extra_tags=file_name[size:])

    return redirect('personal_account')


####  THE REST OF THE CODE IS AVAILABLE TO EMPLOYERS UPON REQUEST. CONTACT ME VIA TELEGRAM, MAIL ####
################################# MORE THEN 200+ LINES OF CODE ######################################
###################################### ESPINOSA ROZOV ALEX ##########################################



















