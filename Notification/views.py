from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import *

@login_required
def home(request):
    current_user = request.user
    if current_user.is_authenticated:
        teacher = Teacher.objects.filter(user=current_user)
        if teacher.exists():
            teacher = teacher.first()
            if teacher.designation == "Principal":
                return render(request, "principal.html")
            else:
                return render(request, "teacher.html")
        elif Student.objects.filter(user=current_user).exists():
            return render(request, "student.html")

    