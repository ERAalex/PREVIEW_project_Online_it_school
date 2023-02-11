from django import forms
from .models import Document, student_model

class DocumentForm(forms.ModelForm):

   class Meta:
      model = Document
      fields = ['docfile']



class StudentForm(forms.ModelForm):

   class Meta:
      model = student_model
      fields = ['user_real_name', 'class_grade_true', 'about_self']







