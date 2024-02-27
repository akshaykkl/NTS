from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.db.models import F
from .models import *
from .forms import *

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
        
    
