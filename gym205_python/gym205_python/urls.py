from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('python_main.urls')),
    path('', include('accounts_cabinet.urls')),
    path('', include('courses.urls')),
]
