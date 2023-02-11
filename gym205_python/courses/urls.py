from django.urls import path
from django.conf import settings
from . import views
from .views import course_python_DetailView, course_html_DetailView, course_multimedia_DetailView

urlpatterns = [
    path('course_python', views.python_course, name='course_python'),
    path('courses/<int:pk>/', course_python_DetailView.as_view(), name='article'),

    path('course_html', views.html_course, name='course_html'),
    path('html/<int:pk>/', course_html_DetailView.as_view(), name='article_html'),

    path('course_multimedia', views.multimedia_course, name='course_multimedia'),
    path('multi/<int:pk>/', course_multimedia_DetailView.as_view(), name='article_html'),

    # загрузка домашнего задания по Python
    path('upload_homework', views.save_homework, name='upload_homework'),

    # загрузка домашнего задания по Html
    path('upload_homework_html', views.save_homework_html, name='upload_homework_html'),

    # загрузка домашнего задания по Multimedia
    path('upload_homework_multimedia', views.save_homework_multimedia, name='upload_homework_multimedia'),

    # удалить урок с заданием Python
    path('del_homework_python/<int:id>/', views.delete_homework_python, name='del_homework_python'),

    # удалить урок с заданием HTML
    path('del_homework_html/<int:id>/', views.delete_homework_html, name='del_homework_html'),

    # удалить урок с заданием Multimedia
    path('del_homework_multimedia/<int:id>/', views.delete_homework_multimedia, name='del_homework_multimedia'),

]