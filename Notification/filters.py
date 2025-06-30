#filers.py
import django_filters
from django import forms
from .models import *
class PrincipalFilterForm(django_filters.FilterSet):
    title = django_filters.CharFilter(
    label='Title',
    lookup_expr='icontains',
    widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    description = django_filters.CharFilter(
    label='Description',
    lookup_expr='icontains',
    widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Media
        fields = ['title', 'description', 'dept', 'student', 'teacher','media_category']


    
    
class TeacherFilterForm(django_filters.FilterSet):
    title = django_filters.CharFilter(
    label='Title',
    lookup_expr='icontains',
    widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    description = django_filters.CharFilter(
    label='Description',
    lookup_expr='icontains',
    widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    class Meta:
        model = TrashMedia
        fields = ['title', 'description', 'dept', 'student', 'teacher', 'media_category']

class PrincipalTrashFilterForm(django_filters.FilterSet):
   
    title = django_filters.CharFilter(
    label='Title',
    lookup_expr='icontains',
    widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    description = django_filters.CharFilter(
    label='Description',
    lookup_expr='icontains',
    widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    class Meta:
        model = Media
        fields = ['title', 'description', 'dept', 'student', 'teacher', 'media_category']

class TeacherTrashFilterForm(django_filters.FilterSet):
    title = django_filters.CharFilter(
    label='Title',
    lookup_expr='icontains',
    widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    description = django_filters.CharFilter(
    label='Description',
    lookup_expr='icontains',
    widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    class Meta:
        model = TrashMedia
        fields = ['title', 'description', 'dept', 'student', 'teacher', 'media_category']

class TeacherFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(
    label='Name',
    lookup_expr='icontains',
    widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    teacher_id = django_filters.CharFilter(
    label='ID',
    lookup_expr='icontains',
    widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    class Meta:
        model = Teacher
        fields = ['name','teacher_id', 'designation', 'dept', 'hod']


class StudentFilter(django_filters.FilterSet):
    dept = django_filters.ModelChoiceFilter(
        queryset=Department.objects.all(),
        label='Department',
        field_name='pgm__dept_id',  # This should match the relationship
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    name = django_filters.CharFilter(
        label='name',
    lookup_expr='icontains',
    widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    admn_no = django_filters.NumberFilter(label='Admission No',
    lookup_expr='icontains',
    widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    class Meta:
        model = Student
        fields = ['name', 'admn_no', 'pgm', 'gender', 'year_of_admission', 'dept']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'admn_no': forms.NumberInput(attrs={'class': 'form-control'}),
            'pgm': forms.Select(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'year_of_admission': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class FeedFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains', label='Title')
    media_category = django_filters.ChoiceFilter(choices=Media.MEDIA_CATEGORY, label='Media Category')

    class Meta:
        model = Media
        fields = ['title', 'media_category']