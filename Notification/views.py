#views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.db.models import F, Q
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.views import PasswordResetView
from django.core.paginator import Paginator

from django.conf import settings
from .models import *
from .forms import *
from .filters import *
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
            'is_principal':(hasattr(request.user, 'teacher') and request.user.teacher.designation=='Principal')
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
            return render(request, 'Notification/error.html',{'access':True})
    return _wrapped_view

@login_required
@add_user_context
def home(request, context):
    try:
        current_user = request.user
        if current_user.is_authenticated:
            return redirect('feed')
    except Exception:
        return render(request, 'Notification/error.html', {'error':True})
            
            
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
                messages.success(request, 'Media Uploaded')
            elif request.POST.get('action') == 'archive':
                media.media_type = 'archive'
                messages.info(request, 'Media Archived')
            media.save()
            
            return redirect('media_upload')
        else:
            form = MediaForm()
    context.update({'form':form})
    return  render(request, 'Notification/media_upload.html', context)

    # except Exception:
    #     return render(request, 'Notification/error.html', {'error':True})

@login_required
@superuser_or_teacher_required
@add_user_context
def uploads_view(request, context):
    try:
        current_user = request.user
        if current_user.is_superuser:
            medias = Media.objects.filter(media_type="upload").order_by('-created_at')
            filter = PrincipalFilterForm(request.GET, queryset=medias)
        else:
            teacher = Teacher.objects.filter(user=current_user).first()
            if teacher:
                if teacher.designation == "Principal":
                    medias = Media.objects.filter(media_type="upload").order_by('-created_at')
                    filter = PrincipalFilterForm(request.GET, queryset=medias)
                else:
                    medias = Media.objects.filter(created_by=current_user, media_type="upload").order_by('-created_at')
                    filter = TeacherFilterForm(request.GET, queryset=medias)
            else:
                medias = Media.objects.none()

        medias = filter.qs
        paginator = Paginator(medias, 5)  # Show 5 media items per page
        page = request.GET.get('page')
        medias_page = paginator.get_page(page)
        context.update({'medias': medias_page, 'filter': filter, 'uploads': 1})
        return render(request, 'Notification/view.html', context)

    except Exception:
        return render(request, 'Notification/error.html', {'error':True})

@add_user_context
@superuser_or_teacher_required
@login_required
def archive_view(request, context):
    try:
        current_user = request.user
        if current_user.is_superuser:
            medias = Media.objects.filter(media_type="archive").order_by('-created_at')
            filter = PrincipalFilterForm(request.GET, queryset=medias)
        else:
            teacher = Teacher.objects.filter(user=current_user).first()
            if teacher:
                medias = Media.objects.filter(created_by=current_user, media_type="archive").order_by('-created_at')
                if teacher.designation == "Principal":
                    filter = PrincipalFilterForm(request.GET, queryset=medias)
                else:
                    filter = TeacherFilterForm(request.GET, queryset=medias)
            else:
                medias = Media.objects.none()

        medias = filter.qs
        paginator = Paginator(medias, 5)  # Show 5 media items per page
        page = request.GET.get('page')
        medias_page = paginator.get_page(page)
        context.update({'medias': medias_page, 'filter': filter, 'archive': 1})
        return render(request, 'Notification/view.html', context)

    except Exception:
        return render(request, 'Notification/error.html', {'error':True})


@add_user_context
@superuser_or_teacher_required
@login_required
def trash_view(request, context):
    try:
        current_user = request.user
        if current_user.is_superuser:
            medias = TrashMedia.objects.all().order_by('-created_at')
            filter = PrincipalTrashFilterForm(request.GET, queryset=medias)
        else:
            teacher = Teacher.objects.filter(user=current_user).first()
            if teacher:
                if teacher.designation == "Principal":
                    medias = TrashMedia.objects.filter(trashed_by=request.user).order_by('-trashed_at')
                    filter = PrincipalTrashFilterForm(request.GET, queryset=medias)
                else:
                    medias = TrashMedia.objects.filter(created_by=current_user).order_by('-created_at')
                    filter = TeacherTrashFilterForm(request.GET, queryset=medias)
            else:
                medias = Media.objects.none()

        medias = filter.qs
        paginator = Paginator(medias, 5)  # Show 5 media items per page
        page = request.GET.get('page')
        medias_page = paginator.get_page(page)
        context.update({'medias': medias_page, 'filter': filter, 'trash': 1})
        return render(request, 'Notification/view.html', context)

    except Exception:
        return render(request, 'Notification/error.html', {'error':True})




@login_required
@add_user_context
def feed(request, context):
    try:
        current_user = request.user
        filterset = FeedFilter(request.GET, queryset=Media.objects.filter(media_type='upload').order_by('-created_at'))
        # Check if the current user is a superuser
        if current_user.is_superuser:
            medias = filterset.qs
            context.update({'medias': medias,'filter':filterset})
            return render(request, 'Notification/feed.html', context)

        # Check if the current user is a teacher
        teacher = Teacher.objects.filter(user=current_user).first()
        if teacher:
            dept = teacher.dept
            medias = filterset.qs.filter(
            Q(teacher=True) &
            (Q(dept=dept) | Q(dept__isnull=True)) &
            Q(media_type='upload')).order_by('-created_at')[:20]
            context.update({'medias': medias,'filter':filterset})
            return render(request, 'Notification/feed.html', context)

        # Assume the current user is a student if not a teacher
        try:
            student = Student.objects.get(user=current_user)
            dept = student.pgm.dept_id
            medias = filterset.qs.filter(
            Q(student=True) &
            (Q(dept=dept) | Q(dept__isnull=True)) &
            Q(media_type='upload')).order_by('-created_at')[:20]
            context.update({'medias': medias,'filter':filterset})
        except Student.DoesNotExist:
            return render(request, 'Notification/error.html')

        return render(request, 'Notification/feed.html', context)

    except Exception:
       return render(request, 'Notification/error.html', {'error':True})
        
    
@login_required
@add_user_context
def profile(request, context):
    try:
        current_user = request.user 
        if current_user.is_superuser:
            admin =  User.objects.get(id=current_user.id)
            print(admin)
            context.update({'admin_details': admin})
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

    except Exception:
        return render(request, 'Notification/error.html', {'error':True})

@login_required
@add_user_context
def change_password(request, context):
    try:
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
                update_session_auth_hash(request, current_user)
                messages.success(request, 'Password Changed')
                return redirect('profile')
            else:
                if 'old_password' in form.errors:
                    messages.error(request, form.errors)
                    
                
        else:
            form = PasswordChangeForm(current_user)
            context.update({'form':form})
            print(form)
        return render(request, 'Notification/change_password.html', context)

    except Exception:
        return render(request, 'Notification/error.html', {'error':True})


@login_required
@add_user_context
def password_reset(request, context, *args, **kwargs):
    try:
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

    except Exception:
        return render(request, 'Notification/error.html', {'error':True})
@login_required
@superuser_or_teacher_required
@add_user_context
def edit_media(request, context, media_id):

        media = Media.objects.get(id=media_id)
        form = MediaEditForm(instance=media)
        if request.method == 'POST':
            form = MediaEditForm(request.POST, request.FILES, instance=media)
            if form.is_valid():
                media1 = form.save(commit=False)
                media1.created_by = media.created_by
                media1_created_at = media.created_at
                media1.save()
                messages.success(request, 'Media item updated successfully!')
                if media.media_type == 'upload':
                    return redirect('uploads_view')
                elif media.media_type == 'archive':
                    return redirect('archive_view')
            else:
                messages.error(request, 'Error updating media item!')
        if media.media_type == 'upload':
            context.update({'upload':True})
        elif media.media_type == 'archive':
            context.update({'archive':True})
        context.update({'form':form, 'media':media})
        return render(request, 'Notification/edit_media.html',context)



@login_required
@superuser_or_teacher_required
@add_user_context
def edit_trash(request, context, media_id):
    try:
        media = TrashMedia.objects.get(id=media_id)
        form = TrashEditForm(instance=media)
        if request.method == 'POST':
            form = TrashEditForm(request.POST, instance=media)
            if form.is_valid():
                media1 = form.save(commit=False)
                media1.created_by = media.created_by
                media1_created_at = media.created_at
                media1.save()
                messages.success(request, 'Trash item updated successfully!')
                return redirect('trash_view')
            else:
                messages.error(request, 'Error updating trash item!')
        context.update({'form':form, 'trash':True,'media':media})
        return render(request, 'Notification/edit_media.html',context)
    except Exception:
        return render(request, 'Notification/error.html', {'error':True})



@login_required
@superuser_or_teacher_required
def move_to_trash(request, media_id):
    try:
        if request.method == 'GET':
            try:
                media = Media.objects.get(id=media_id)
                if media.media_type == 'upload':
                    media.move_to_trash(request.user)
                    messages.success(request, 'Media item moved to trash successfully!')
                    return redirect('uploads_view')
                elif media.media_type == 'archive':
                    media.move_to_trash(request.user)
                    messages.success(request, 'Media item moved to trash successfully!')
                    return redirect('archive_view')
            except:
                messages.error(request, 'Error moving media item to trash!')
            return redirect('uploads_view')

    except Exception:
        return render(request, 'Notification/error.html', {'error':True})

@login_required
@superuser_or_teacher_required
def delete_media(request, media_id):
    try:
        if request.method == 'GET':
            try:
                media = get_object_or_404(TrashMedia, id=media_id)
                media.delete()
                messages.success(request, 'Media item deleted successfully!')
                return redirect('trash_view')
            except TrashMedia.DoesNotExist:
                messages.error(request, 'Error deleting media item!')
                return redirect('trash_view')
            except Exception as e:
                messages.error(request, 'Error deleting media item!')
                return redirect('trash_view')
                
        else:
            return HttpResponseBadRequest('Invalid request method.')

    except Exception:
        return render(request, 'Notification/error.html', {'error':True})
    
@login_required
@superuser_or_teacher_required
def swap_type(request, media_id):
    try:
        if request.method == 'GET':
            try:
                media = Media.objects.get(id=media_id)
                if media.media_type == 'upload':
                    media.media_type = 'archive'
                    media.save()
                    messages.success(request, 'In Archive')
                    return redirect('uploads_view')
                elif media.media_type == 'archive':
                    media.media_type = 'upload'
                    media.save()
                    messages.success(request, 'In Uploads')
                    return redirect('archive_view')
            except Media.DoesNotExist:
                return HttpResponseBadRequest('Media not found!')
            except Exception as e:
                return HttpResponseBadRequest(f'An error occurred: {e}')
        else:
            return HttpResponseBadRequest('Invalid request method.')

    except Exception:
        return render(request, 'Notification/error.html', {'error':True})

@login_required
@superuser_or_teacher_required
def restore(request, media_id):
    try:
        if request.method == 'GET':
            try:
                media = TrashMedia.objects.get(id=media_id)
                media.restore()
                messages.success(request, 'Item restored!')
            except:
                messages.error(request, 'Error restoring item!')
        return redirect('trash_view')

    except Exception:
        return render(request, 'Notification/error.html', {'error':True})

@login_required
@superuser_or_teacher_required
@add_user_context
def teachers(request, context):
    try:
        teachers = Teacher.objects.all()
        filter = TeacherFilter(request.GET, queryset=teachers)
        teachers = filter.qs
        context.update({'teachers':teachers, 'filter':filter, 'teacher':True})
        return render(request, 'Notification/showusers.html', context)

    except Exception:
        return render(request, 'Notification/error.html', {'error':True})

@login_required
@superuser_or_teacher_required
@add_user_context
def students(request, context):
    try:
        students_queryset = Student.objects.all()
        student_filter = StudentFilter(request.GET, queryset=students_queryset)
        
        # Pagination
        paginator = Paginator(student_filter.qs, 10)  # Show 10 students per page
        page_number = request.GET.get('page')
        students_page = paginator.get_page(page_number)
        
        context.update({'students': students_page, 'filter': student_filter, 'student': True})
        
        return render(request, 'Notification/showusers.html', context)

    except Exception:
       return render(request, 'Notification/error.html', {'error':True})

@login_required
@superuser_or_teacher_required
@add_user_context
def manage_teacher(request, context, teacher_id=None):
    try:
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
                user_form = UserEditForm(request.POST, instance=user)
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
                messages.success(request, 'Updated')
                return redirect('teachers')  # Redirect to a success page
        else:
            if teacher:
                user_form = UserEditForm(instance=user)
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

    except Exception:
        return render(request, 'Notification/error.html', {'error':True})


@login_required
@superuser_or_teacher_required
@add_user_context
def manage_student(request, context, student_id=None):
    try:
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
                user_form = UserEditForm(request.POST, instance=user)
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
                messages.success(request, 'Updated')
                return redirect('students')  # Redirect to a success page
        else:
            if student:
                user_form = UserEditForm(instance=user)
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

    except Exception:
        return render(request, 'Notification/error.html', {'error':True})

@login_required
@superuser_or_teacher_required
def delete_teacher(request, teacher_id):
    try:
        teacher = get_object_or_404(Teacher, id=teacher_id)
        print(teacher)
        teacher.user.delete()  # This deletes the associated user as well.
        teacher.delete()
        messages.success(request, 'Deleted')
        return redirect('teachers')  # Replace 'teacher_list' with your actual URL name for the list of teachers.

    except Exception:
        return render(request, 'Notification/error.html')

@login_required
@superuser_or_teacher_required
def delete_student(request, student_id):
    try:
        student = get_object_or_404(Student, id=student_id)
        print(student)
        student.user.delete()  # This deletes the associated user as well.
        student.delete()
        messages.success(request, 'Deleted')
        return redirect('students')  # Replace 'student_list' with your actual URL name for the list of students.

    except Exception:
        return render(request, 'Notification/error.html', {'error':True})

@login_required
@superuser_or_teacher_required
@add_user_context 
def department_list(request, context):
    try:
        departments = Department.objects.all()
        context.update({'departments': departments})
        return render(request, 'Notification/department_list.html', context)

    except Exception:
        return render(request, 'Notification/error.html')

@login_required
@superuser_or_teacher_required
@add_user_context 
def programme_list(request, context):
    try:
        programmes = Programme.objects.all()
        context.update({'programmes': programmes})
        return render(request, 'Notification/programme_list.html', context)

    except Exception:
        return render(request, 'Notification/error.html', {'error':True})

@login_required
@superuser_or_teacher_required
@add_user_context 
def add_edit_department(request, context, department_id=None):
    try:
        if department_id:
            department = get_object_or_404(Department, id=department_id)
        else:
            department = None

        if request.method == 'POST':
            form = DepartmentForm(request.POST, instance=department)
            if form.is_valid():
                form.save()
                messages.success(request, 'Saved')
                return redirect('departments')  
        else:
            form = DepartmentForm(instance=department)
        context.update({'form': form})
        return render(request, 'Notification/department_form.html', context)

    except Exception:
        return render(request, 'Notification/error.html', {'error':True})

@login_required
@superuser_or_teacher_required
@add_user_context
def add_edit_programme(request, context,programme_id=None):
    try:
        if programme_id:
            programme = get_object_or_404(Programme, id=programme_id)
        else:
            programme = None

        if request.method == 'POST':
            form = ProgrammeForm(request.POST, instance=programme)
            if form.is_valid():
                form.save()
                messages.success(request, 'Saved')
                return redirect('programmes') 
        else:
            form = ProgrammeForm(instance=programme)
        context.update({'form':form})
        return render(request, 'Notification/programme_form.html', context)

    except Exception:
        return render(request, 'Notification/error.html', {'error':True})