# In forms.py
from django import forms
from .models import *

class MediaForm(forms.ModelForm):
    class Meta:
        model = Media
        fields = ['title', 'description', 'media_type', 'file','student','teacher', 'pgm']
