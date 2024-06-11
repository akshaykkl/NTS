# In forms.py
from django import forms
from django.conf import settings
from .models import *


class MediaForm(forms.ModelForm):
    class Meta:
        model = Media
        fields = ['title', 'description', 'media_type', 'file','student','teacher', 'dept']

class MediaEditForm(forms.ModelForm):
    class Meta:
        model = Media
        exclude = ['uploaded_by', 'uploaded_at']

class MediaFilterForm(forms.Form):
    title = forms.CharField(required=False)
    dept = forms.ModelMultipleChoiceField(
        queryset=Department.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={'size': 10})
    )
    uploaded_by = forms.ModelMultipleChoiceField(
        queryset=Teacher.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={'size':10})
    )
