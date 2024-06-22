import django_filters
from django import forms
from .models import *
class PrincipalFilterForm(django_filters.FilterSet):
    class Meta:
        model = Media
        fields = ['title', 'description', 'created_at', 'created_by', 'dept', 'student', 'teacher']


    
    
class TeacherFilterForm(django_filters.FilterSet):
    
    class Meta:
        model = TrashMedia
        fields = ['title', 'description', 'created_at', 'dept', 'student', 'teacher']

class PrincipalTrashFilterForm(django_filters.FilterSet):
   

    class Meta:
        model = Media
        fields = ['title', 'description', 'created_at', 'created_by', 'dept', 'student', 'teacher']

class TeacherTrashFilterForm(django_filters.FilterSet):
  
    class Meta:
        model = TrashMedia
        fields = ['title', 'description', 'created_at', 'dept', 'student', 'teacher']

class TeacherFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(
    label='Name',
    lookup_expr='icontains',
    widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    class Meta:
        model = Teacher
        fields = ['name', 'designation', 'dept']


class StudentFilter(django_filters.FilterSet):
    dept = django_filters.ModelChoiceFilter(
        queryset=Department.objects.all(),
        label='Department',
        field_name='pgm__dept_id',  # This should match the relationship
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        name = django_filters.CharFilter(
        lookup_expr='icontains',
        widget=forms.TextInput(attrs={'class': 'form-control'})
        )
        admn_no = django_filters.NumberFilter(
        lookup_expr='icontains',
        widget=forms.NumberInput(attrs={'class': 'form-control'})
        )
        model = Student
        fields = ['name', 'admn_no', 'pgm', 'gender', 'year_of_admission', 'dept']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'admn_no': forms.NumberInput(attrs={'class': 'form-control'}),
            'pgm': forms.Select(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'year_of_admission': forms.NumberInput(attrs={'class': 'form-control'}),
        }