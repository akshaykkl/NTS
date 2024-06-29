from django.urls import path, include
from django.conf.urls.static import static

from .views import *
urlpatterns = [
    path('',home, name="home"),
    path('upload/', media_upload, name= 'media_upload'),
    path('uploads/', uploads_view, name="uploads_view"),
    path('archive/', archive_view, name="archive_view"),
    path('trash/', trash_view, name="trash_view"),
    path('feed/', feed, name='feed'),
    path('profile/', profile, name="profile"),
    path('change_password/', change_password, name="change_password"),
    path('password-reset/', password_reset, name='password_reset'),
    path('edit_media<int:media_id>/', edit_media, name="edit_media"),
    path('edit_trash<int:media_id>/', edit_trash, name="edit_trash"),
    path('move_to_trash<int:media_id>/', move_to_trash, name="move_to_trash"),
    path('delete_media<int:media_id>', delete_media, name='delete_media'),
    path('swap_type<int:media_id>', swap_type, name='swap_type'),
    path('restore<int:media_id>', restore, name='restore'),
    path('teachers/', teachers, name='teachers'),
    path('teacher/manage/', manage_teacher, name='add_teacher'),
    path('teacher/manage/<int:teacher_id>/', manage_teacher, name='edit_teacher'),
    path('students/', students, name='students'),
    path('student/manage/', manage_student, name='add_student'),
    path('student/manage/<int:student_id>/', manage_student, name='edit_student'),
    path('departments/', department_list, name='departments'),
    path('department/', add_edit_department, name='add_department'),
    path('department/<int:department_id>/', add_edit_department, name='edit_department'),
    path('programmes/', programme_list, name='programmes'),
    path('programme/', add_edit_programme, name='add_programme'),
    path('programme/<int:programme_id>/', add_edit_programme, name='edit_programme'),
    path('delete_teacher/<int:teacher_id>/', delete_teacher, name='delete_teacher'),
    path('delete_student/<int:student_id>/', delete_student, name='delete_student'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


