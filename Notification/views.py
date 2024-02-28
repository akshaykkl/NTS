from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.views import PasswordResetView
from django.conf import settings
from .models import *
from .forms import *
from .utils import *

@login_required
def home(request):
    current_user = request.user
    if current_user.is_authenticated:
        '''if current_user.is_superuser:
            return redirect("admin")'''
        teacher = Teacher.objects.filter(user=current_user)
        if teacher.exists():
            teacher = teacher.first()
            if teacher.designation == "principal":
                principal = 1
                return render(request, "base.html", {"principal" : principal})
            else:
                teacher = 1
                return render(request, "base.html",{"teacher": teacher})
        elif Student.objects.filter(user=current_user).exists():
            student = 1
            return render(request, "base.html",{'student':student})
        else:
            return HttpResponse("You are not meant to access this page")
            
@login_required
def media_upload(request):
    form = MediaForm()
    current_user = request.user
    if request.method == 'POST':
        form = MediaForm(request.POST,request.FILES)
        if form.is_valid():
            media = form.save(commit=False)
            media.uploaded_by = request.user
            media.save()
        else:
            form = MediaForm()
    teacher = Teacher.objects.filter(user=current_user)
    teacher = teacher.first()
    if teacher.designation == 'principal':
        context = {
            'form':form,
            'principal':1
        }
        return  render(request, 'Notification/media_upload.html', context)
    else:
        context = {
            'form':form,
            'teacher':1
        }
        return  render(request, 'Notification/media_upload.html', context)

@login_required
def teacher_view(request):
    current_user = request.user
    if current_user.is_authenticated:
        teacher = Teacher.objects.filter(user=current_user)
        if teacher.exists:
            teacher = teacher.first()
            if teacher.designation == "principal":
                medias = Media.objects.all().order_by('uploaded_at')
                context = {
                    'medias':medias,
                    'principal':1
                }
                return render(request,'Notification/view.html',context)
            else:
                medias = Media.objects.filter(uploaded_by=current_user).order_by('-uploaded_at')
                context = {
                    'medias':medias,
                    'teacher':1
                }
                return render(request,'Notification/view.html',context)

@login_required        
def feed(request):
    current_user = request.user
    teacher = Teacher.objects.filter(user=current_user)
    if teacher.exists():
        medias = Media.objects.filter(teacher=True).order_by(F('uploaded_at').desc())[:20]
        context = {
            'medias':medias,
            'teacher':1,
            'principal':1
        }
        return render(request,'Notification/feed.html',context)
    else:
        student = Student.objects.filter(user=current_user).first()
        programme = student.pgm
        print(programme)
        medias = Media.objects.filter(student=True,pgm=programme).order_by(F('uploaded_at').desc())[:20]
        context = {
            'medias':medias,
        }
        return render(request,'Notification/feed.html',context)
        
    
@login_required
def profile(request):
    current_user = request.user
    context = {"user": current_user}
    
    try:
        teacher = Teacher.objects.get(user=current_user)
        context.update({"teacher": 1, "teacher_details": teacher})
    except Teacher.DoesNotExist:
        pass
    
    try:
        student = Student.objects.get(user=current_user)
        context.update({"student": 1, "student_details": student})
    except Student.DoesNotExist:
        pass
    
    return render(request, "Notification/profile.html", context)

def change_password(request):
    current_user = request.user
    context = {"user": current_user}
    
    try:
        teacher = Teacher.objects.get(user=current_user)
        context.update({"teacher": 1, "teacher_details": teacher})
    except Teacher.DoesNotExist:
        pass
    
    try:
        student = Student.objects.get(user=current_user)
        context.update({"student": 1, "student_details": student})
    except Student.DoesNotExist:
        pass
    if request.method == 'POST':
        form = PasswordChangeForm(current_user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, current_user)  # Keep the user logged in
            return redirect('profile')
    else:
        form = PasswordChangeForm(current_user)
        context.update({'form':form})
    return render(request, 'Notification/change_password.html', context)




def password_reset(request, *args, **kwargs):
    current_user = request.user
    context = {"user": current_user}
    
    try:
        teacher = Teacher.objects.get(user=current_user)
        context.update({"teacher": 1, "teacher_details": teacher})
    except Teacher.DoesNotExist:
        pass
    
    try:
        student = Student.objects.get(user=current_user)
        context.update({"student": 1, "student_details": student})
    except Student.DoesNotExist:
        pass
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            if send_password_reset_email(request, email):
                return render(request, 'Notification/password_reset_done.html')
    else:
        form = PasswordResetForm()
        context.update({'form':form})
    return render(request, 'Notification/password_reset.html', context)