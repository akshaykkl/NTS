from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseBadRequest
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

def superuser_or_teacher_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        user = request.user
        if user.is_superuser or hasattr(user, 'teacher'):
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseBadRequest("Bad Request: You do not have permission to access this page.")
    return _wrapped_view

@login_required
@add_user_context
def home(request, context):
    current_user = request.user
    if current_user.is_authenticated:
        return render(request, 'base.html', context)
            
            
@login_required
@superuser_or_teacher_required
@add_user_context
def media_upload(request, context):
    form = MediaForm()
    current_user = request.user
    if request.method == 'POST':
        form = MediaForm(request.POST,request.FILES)
        if form.is_valid():
            media = form.save(commit=False)
            media.created_by = request.user
            if request.POST.get('action') == 'upload':
                media.media_type = 'upload'
            elif request.POST.get('action') == 'archive':
                media.media_type = 'archive'
            media.save()
            return redirect('media_upload')
        else:
            form = MediaForm()
    context.update({'form':form})
    return  render(request, 'Notification/media_upload.html', context)
    

@login_required
@superuser_or_teacher_required
@add_user_context
def uploads_view(request, context):
    current_user = request.user
    form = PrincipalFilterForm(request.GET or None)
    
    # Check if the user is a superuser
    if current_user.is_superuser:
        medias = Media.objects.filter(media_type="upload").order_by('created_at')
    else:
        # Check if the user is a teacher
        teacher = Teacher.objects.filter(user=current_user).first()
        if teacher:
            if teacher.designation == "principal":
                medias = Media.objects.filter(media_type="upload").order_by('created_at')
            else:
                form = TeacherFilterForm(request.GET or None)
                medias = Media.objects.filter(created_by=current_user, media_type="upload").order_by('created_at')
        else:
            medias = Media.objects.none()

    # Apply filters from the form if it is valid
    if form.is_valid():
        title = form.cleaned_data.get('title')
        dept = form.cleaned_data.get('dept')
        created_by = form.cleaned_data.get('created_by')
        
        if title:
            medias = medias.filter(title__icontains=title)
        if dept:
            medias = medias.filter(dept__in=dept)
        if created_by:
            user_ids = created_by.values_list('user_id', flat=True)
            medias = medias.filter(created_by__in=user_ids)

    context.update({'medias': medias, 'form': form, 'uploads':1})
    return render(request, 'Notification/view.html', context)


@add_user_context
@superuser_or_teacher_required
@login_required
def archive_view(request, context):
    current_user = request.user
    form = PrincipalFilterForm(request.GET or None)
    
    # Check if the user is a superuser
    if current_user.is_superuser:
        medias = Media.objects.filter(media_type="archive").order_by('created_at')
    else:
        # Check if the user is a teacher
        teacher = Teacher.objects.filter(user=current_user).first()
        if teacher:
            if teacher.designation == "principal":
                medias = Media.objects.filter(media_type="archive").order_by('created_at')
            else:
                form = TeacherFilterForm(request.GET or None)
                medias = Media.objects.filter(created_by=current_user, media_type="archive").order_by('created_at')
        else:
            medias = Media.objects.none()

    # Apply filters from the form if it is valid
    if form.is_valid():
        title = form.cleaned_data.get('title')
        dept = form.cleaned_data.get('dept')
        created_by = form.cleaned_data.get('created_by')
        
        if title:
            medias = medias.filter(title__icontains=title)
        if dept:
            medias = medias.filter(dept__in=dept)
        if created_by:
            user_ids = created_by.values_list('user_id', flat=True)
            medias = medias.filter(created_by__in=user_ids)

    context.update({'medias': medias, 'form': form, 'archive':1})
    return render(request, 'Notification/view.html', context)


@add_user_context
@superuser_or_teacher_required
@login_required
def trash_view(request, context):
    current_user = request.user
    form = PrincipalFilterForm(request.GET or None)
    
    # Check if the user is a superuser
    if current_user.is_superuser:
        medias = TrashMedia.objects.filter().order_by('created_at')
    else:
        # Check if the user is a teacher
        teacher = Teacher.objects.filter(user=current_user).first()
        if teacher:
            if teacher.designation == "principal":
                medias = TrashMedia.objects.filter(trashed_by=request.user).order_by('trashed_at')
            else:
                form = TeacherFilterForm(request.GET or None)
                medias = TrashMedia.objects.filter(created_by=current_user).order_by('created_at')
        else:
            medias = Media.objects.none()

    # Apply filters from the form if it is valid
    if form.is_valid():
        title = form.cleaned_data.get('title')
        dept = form.cleaned_data.get('dept')
        created_by = form.cleaned_data.get('created_by')
        
        if title:
            medias = medias.filter(title__icontains=title)
        if dept:
            medias = medias.filter(dept__in=dept)
        if created_by:
            user_ids = created_by.values_list('user_id', flat=True)
            medias = medias.filter(created_by__in=user_ids)

    context.update({'medias': medias, 'form': form, 'trash': 1})
    return render(request, 'Notification/view.html', context)



@login_required
@add_user_context
def feed(request, context):
    current_user = request.user

    # Check if the current user is a superuser
    if current_user.is_superuser:
        medias = Media.objects.filter(media_type='upload').order_by('created_at')
        context.update({'medias': medias})
        return render(request, 'Notification/feed.html', context)

    # Check if the current user is a teacher
    teacher = Teacher.objects.filter(user=current_user).first()
    if teacher:
        dept = teacher.dept
        medias = Media.objects.filter(
        Q(teacher=True) &
        (Q(dept=dept) | Q(dept__dept_name="All")) &
        Q(media_type='upload')).order_by('-created_at')[:20]
        context.update({'medias': medias})
        return render(request, 'Notification/feed.html', context)

    # Assume the current user is a student if not a teacher
    try:
        student = Student.objects.get(user=current_user)
        dept = student.pgm.dept_id
        medias = Media.objects.filter(
        Q(student=True) &
        (Q(dept=dept) | Q(dept__dept_name="All")) &
        Q(media_type='upload')).order_by('-created_at')[:20]
        context.update({'medias': medias})
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
@superuser_or_teacher_required
@add_user_context
def edit_media(request, context, media_id):
    media = Media.objects.get(id=media_id)
    form = MediaEditForm(instance=media)
    if request.method == 'POST':
        form = MediaEditForm(request.POST, instance=media)
        if form.is_valid():
            media1 = form.save(commit=False)
            media1.created_by = media.created_by
            media1_created_at = media.created_at
            media1.save()
            #messages.success(request, 'Media item updated successfully!')
            if media.media_type == 'upload':
                return redirect('uploads_view')
            elif media.media_type == 'archive':
                return redirect('archive_view')
    if media.media_type == 'upload':
        context.update({'upload':True})
    elif media.media_type == 'archive':
        context.update({'archive':True})
    context.update({'form':form})
    return render(request, 'Notification/edit_media.html',context)

@login_required
@superuser_or_teacher_required
@add_user_context
def edit_trash(request, context, media_id):
    media = TrashMedia.objects.get(id=media_id)
    form = TrashEditForm(instance=media)
    if request.method == 'POST':
        form = TrashEditForm(request.POST, instance=media)
        if form.is_valid():
            media1 = form.save(commit=False)
            media1.created_by = media.created_by
            media1_created_at = media.created_at
            media1.save()
            #messages.success(request, 'Media item updated successfully!')
            return redirect('trash_view')
    context.update({'form':form, 'trash':True})
    return render(request, 'Notification/edit_media.html',context)


@login_required
@superuser_or_teacher_required
@add_user_context
def view_media(request, context, media_id):
    media = Media.objects.get(id=media_id)
    context.update({'media':media})
    return render(request, 'Notification/view_media.html', context)

@login_required
@superuser_or_teacher_required
def move_to_trash(request, media_id):
    if request.method == 'GET':
        try:
            media = Media.objects.get(id=media_id)
            media.move_to_trash(request.user)
        except:
            pass
        return redirect('uploads_view')
    else:
        return HttpResponse('Error Occured')

@login_required
@superuser_or_teacher_required
def delete_media(request, media_id):
    if request.method == 'GET':
        try:
            media = get_object_or_404(TrashMedia, id=media_id)
            print('\n\n\n')
            media.delete()
            return redirect('trash_view')
        except TrashMedia.DoesNotExist:
            return HttpResponseBadRequest('Media not found.')
        except Exception as e:
            return HttpResponseBadRequest(f'An error occurred: {e}')
    else:
        return HttpResponseBadRequest('Invalid request method.')

@login_required
@superuser_or_teacher_required
def swap_type(request, media_id):
    if request.method == 'GET':
        try:
            media = Media.objects.get(id=media_id)
            if media.media_type == 'upload':
                media.media_type = 'archive'
                media.save()
                return redirect('uploads_view')
            elif media.media_type == 'archive':
                media.media_type = 'upload'
                media.save()
                return redirect('archive_view')
            return HttpResponse('Media type swapped successfully.')
        except Media.DoesNotExist:
            return HttpResponseBadRequest('Media not found.')
        except Exception as e:
            return HttpResponseBadRequest(f'An error occurred: {e}')
    else:
        return HttpResponseBadRequest('Invalid request method.')

@login_required
@superuser_or_teacher_required
def restore(request, media_id):
    if request.method == 'GET':
        try:
            media = TrashMedia.objects.get(id=media_id)
            media.restore()
        except:
            pass
    return redirect('trash_view')

@login_required
@superuser_or_teacher_required
@add_user_context
def teachers(request, context):
    teachers = Teacher.objects.all()
    context.update({'teachers':teachers,'teacher':True})
    return render(request, 'Notification/showusers.html', context)

@login_required
@superuser_or_teacher_required
@add_user_context
def students(request, context):
    students = Student.objects.all()
    context.update({'students':students, 'student':True})
    return render(request, 'Notification/showusers.html', context)


@login_required
@superuser_or_teacher_required
@add_user_context
def manage_teacher(request, context, teacher_id=None):
    if teacher_id:
        teacher = get_object_or_404(Teacher, pk=teacher_id)
        user = teacher.user
        if request.user.is_superuser or request.user == user:
            pass
        else:
            return HttpResponseBadRequest("You are not authorized to edit this teacher.")
    else:
        teacher = None
        user = None

    if request.method == 'POST':
        if teacher:
            user_form = UserForm(request.POST, instance=user)
            teacher_form = TeacherForm(request.POST, instance=teacher)
        else:
            user_form = UserForm(request.POST)
            teacher_form = TeacherForm(request.POST)

        if user_form.is_valid() and teacher_form.is_valid():
            user = user_form.save(commit=False)
            if not teacher:
                user.set_password(user_form.cleaned_data['password'])
            user.save()

            teacher = teacher_form.save(commit=False)
            teacher.user = user
            teacher.save()

            return redirect('some_view_name')  # Redirect to a success page
    else:
        if teacher:
            user_form = UserForm(instance=user)
            teacher_form = TeacherForm(instance=teacher)
        else:
            user_form = UserForm()
            teacher_form = TeacherForm()

    context.update({
        'user_form': user_form,
        'teacher_form': teacher_form,
        'teacher': teacher,
    })
    return render(request, 'Notification/teacher.html', context)


@login_required
@superuser_or_teacher_required
@add_user_context
def manage_student(request, context, student_id=None):
    if student_id:
        student = get_object_or_404(Student, pk=student_id)
        user = student.user
        if request.user.is_superuser or request.user == user:
            pass
        else:
            return HttpResponseBadRequest("You are not authorized to edit this student.")
    else:
        student = None
        user = None

    if request.method == 'POST':
        if student:
            user_form = UserForm(request.POST, instance=user)
            student_form = StudentForm(request.POST, instance=student)
        else:
            user_form = UserForm(request.POST)
            student_form = StudentForm(request.POST)

        if user_form.is_valid() and student_form.is_valid():
            user = user_form.save(commit=False)
            if not student:
                user.set_password(user_form.cleaned_data['password'])
            user.save()

            student = student_form.save(commit=False)
            student.user = user
            student.save()

            return redirect('some_view_name')  # Redirect to a success page
    else:
        if student:
            user_form = UserForm(instance=user)
            student_form = StudentForm(instance=student)
        else:
            user_form = UserForm()
            student_form = StudentForm()

    context.update({
        'user_form': user_form,
        'student_form': student_form,
        'student': student,
    })
    return render(request, 'Notification/student.html', context)

@login_required
@superuser_or_teacher_required
def delete_teacher(request, teacher_id):
    teacher = get_object_or_404(Teacher, id=teacher_id)
    print(teacher)
    teacher.user.delete()  # This deletes the associated user as well.
    teacher.delete()
    return redirect('teachers')  # Replace 'teacher_list' with your actual URL name for the list of teachers.

@login_required
@superuser_or_teacher_required
def delete_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    print(student)
    student.user.delete()  # This deletes the associated user as well.
    student.delete()
    return redirect('students')  # Replace 'student_list' with your actual URL name for the list of students.

@login_required
@superuser_or_teacher_required
@add_user_context 
def department_list(request, context):
    departments = Department.objects.all()
    context.update({'departments': departments})
    return render(request, 'Notification/department_list.html', context)

@login_required
@superuser_or_teacher_required
@add_user_context 
def programme_list(request, context):
    programmes = Programme.objects.all()
    context.update({'programmes': programmes})
    return render(request, 'Notification/programme_list.html', context)


@login_required
@superuser_or_teacher_required
@add_user_context 
def add_edit_department(request, context, department_id=None):
    if department_id:
        department = get_object_or_404(Department, id=department_id)
    else:
        department = None

    if request.method == 'POST':
        form = DepartmentForm(request.POST, instance=department)
        if form.is_valid():
            form.save()
            #return redirect('Notification/department_list')  # Adjust the redirect as needed
    else:
        form = DepartmentForm(instance=department)
    context.update({'form': form})
    return render(request, 'Notification/department_form.html', context)

@login_required
@superuser_or_teacher_required
@add_user_context
def add_edit_programme(request, context,programme_id=None):
    if programme_id:
        programme = get_object_or_404(Programme, id=programme_id)
    else:
        programme = None

    if request.method == 'POST':
        form = ProgrammeForm(request.POST, instance=programme)
        if form.is_valid():
            form.save()
            #return redirect('Notification/programme_list')  # Adjust the redirect as needed
    else:
        form = ProgrammeForm(instance=programme)
    context.update({'form':form})
    return render(request, 'Notification/programme_form.html', context)