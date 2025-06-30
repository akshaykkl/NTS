# In forms.py
from django import forms
from django.contrib.auth.models import User
from .models import *


class MediaForm(forms.ModelForm):
    class Meta:
        model = Media
        fields = ['title', 'description', 'file', 'dept', 'student','teacher', 'media_category']

class MediaEditForm(forms.ModelForm):
    class Meta:
        model = Media
        exclude = ['created_by', 'created_at', 'media_type']

class TrashEditForm(forms.ModelForm):
    class Meta:
        model = TrashMedia
        exclude = ['created_by', 'created_at', 'media_type','trashed_by', 'trashed_at']



class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class UserEditForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username', 'email']

class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['name', 'designation', 'dept', 'hod']

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['admn_no', 'name', 'gender', 'year_of_admission', 'pgm', 'current_sem', 'status']

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['dept_name']

class ProgrammeForm(forms.ModelForm):
    class Meta:
        model = Programme
        fields = ['pgm_name', 'grad_level', 'dept_id']
        