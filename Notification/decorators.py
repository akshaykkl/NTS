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