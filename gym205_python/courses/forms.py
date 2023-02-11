from django import forms
from .models import homework_python, homework_html, homework_multimedia


class Homework_pythonForm(forms.ModelForm):
   class Meta:
      model = homework_python
      fields = ['name_lesson', 'file_lesson']



class Homework_htmlForm(forms.ModelForm):
   class Meta:
      model = homework_html
      fields = ['name_lesson', 'file_lesson']



class Homework_multimediaForm(forms.ModelForm):
   class Meta:
      model = homework_multimedia
      fields = ['name_lesson', 'file_lesson']