from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.db.models import F, Q
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.views import PasswordResetView
from django.conf import settings
from .models import *
from .forms import *
from .utils import *
from functools import wraps

def add_user_context(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        context = {
            'user': request.user,
            'is_superuser': request.user.is_superuser,
            'is_teacher': hasattr(request.user, 'teacher'),
            'is_student': hasattr(request.user, 'student'),
        }
        return view_func(request, context, *args, **kwargs)
    return _wrapped_view


@login_required
@add_user_context
def home(request, context):
    current_user = request.user
    if current_user.is_authenticated:
        return redirect(feed)
            
            
@login_required
@add_user_context
def media_upload(request, context):
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
    context.update({'form':form})
    return  render(request, 'Notification/media_upload.html', context)
    

@login_required
@add_user_context
def teacher_view(request, context):
    form = MediaFilterForm(request.GET or None)
    current_user = request.user
    
    # Check if the user is a superuser
    if current_user.is_superuser:
        medias = Media.objects.all().order_by('uploaded_at')
    else:
        # Check if the user is a teacher
        teacher = Teacher.objects.filter(user=current_user).first()
        if teacher:
            if teacher.designation == "principal":
                medias = Media.objects.all().order_by('uploaded_at')
            else:
                medias = Media.objects.filter(uploaded_by=current_user).order_by('uploaded_at')
        else:
            medias = Media.objects.none()

    # Apply filters from the form if it is valid
    if form.is_valid():
        title = form.cleaned_data.get('title')
        dept = form.cleaned_data.get('dept')
        uploaded_by = form.cleaned_data.get('uploaded_by')
        
        if title:
            medias = medias.filter(title__icontains=title)
        if dept:
            medias = medias.filter(dept__in=dept)
        if uploaded_by:
            user_ids = uploaded_by.values_list('user_id', flat=True)
            medias = medias.filter(uploaded_by__in=user_ids)

    context.update({'medias': medias, 'form': form})
    return render(request, 'Notification/view.html', context)

@login_required
@add_user_context
def feed(request, context):
    current_user = request.user

    # Check if the current user is a superuser
    if current_user.is_superuser:
        medias = Media.objects.all().order_by('uploaded_at')
        context.update({'medias': medias})
        return render(request, 'Notification/feed.html', context)

    # Check if the current user is a teacher
    teacher = Teacher.objects.filter(user=current_user).first()
    if teacher:
        dept = teacher.dept
        medias = Media.objects.filter(Q(teacher=True) & (Q(dept=dept) | Q(dept__dept_name="All"))
        ).order_by(F('uploaded_at').desc())[:20]
        context.update({'medias': medias})
        return render(request, 'Notification/feed.html', context)

    # Assume the current user is a student if not a teacher
    try:
        student = Student.objects.get(user=current_user)
        dept = student.pgm.dept_id
        medias = Media.objects.filter(Q(student=True) & (Q(dept=dept) | Q(dept__dept_name="All"))
        ).order_by(F('uploaded_at').desc())[:20]
        context.update({'medias': medias})
    except Student.DoesNotExist:
        return render(request, 'Notification/error.html')

    return render(request, 'Notification/feed.html', context)
        
    
@login_required
@add_user_context
def profile(request, context):
    current_user = request.user    
    try:
        teacher = Teacher.objects.get(user=current_user)
        context.update({"teacher_details": teacher})
    except Teacher.DoesNotExist:
        pass
    
    try:
        student = Student.objects.get(user=current_user)
        context.update({"student_details": student})
    except Student.DoesNotExist:
        pass
    
    return render(request, "Notification/profile.html", context)

@login_required
@add_user_context
def change_password(request, context):
    current_user = request.user

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
            return render(request, 'Notification/change_password.html', {'context':context,'form':form})
    else:
        form = PasswordChangeForm(current_user)
    return render(request, 'Notification/change_password.html', {'context':context,'form':form})


@login_required
@add_user_context
def password_reset(request, context, *args, **kwargs):
    current_user = request.user
    
    try:
        teacher = Teacher.objects.get(user=current_user)
        context.update({"teacher_details": teacher})
    except Teacher.DoesNotExist:
        pass
    
    try:
        student = Student.objects.get(user=current_user)
        context.update({"student_details": student})
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

@login_required
@add_user_context
def edit_media(request, context, media_id):
    media = Media.objects.get(id=media_id)
    form = MediaEditForm(instance=media)
    if request.method == 'POST':
        form = MediaEditForm(request.POST, instance=media)
        if form.is_valid():
            media1 = form.save(commit=False)
            media1.uploaded_by = media.uploaded_by
            media1_uploaded_at = media.uploaded_at
            media1.save()
            #messages.success(request, 'Media item updated successfully!')
            return redirect('teacher_view')
    context.update({'form':form})
    return render(request, 'Notification/edit_media.html',context)

@login_required
@add_user_context
def view_media(request, context, media_id):
    media = Media.objects.get(id=media_id)
    context.update({'media':media})
    return render(request, 'Notification/view_media.html', context)

@login_required
@add_user_context
def delete_media(request, context, media_id):
    if request.method == 'GET':
        try:
            media = Media.objects.get(id=media_id)
            media.delete()
        except:
            pass
        return redirect('teacher_view')
    else:
        return HttpResponse('Error Occured')
