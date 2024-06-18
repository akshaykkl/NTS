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
    path('view_media<int:media_id>/', view_media, name="view_media"),
    path('move_to_trash<int:media_id>/', move_to_trash, name="move_to_trash"),
    path('delete_media<int:media_id>', delete_media, name='delete_media'),
    path('swap_type<int:media_id>', swap_type, name='swap_type'),
    path('restore<int:media_id>', restore, name='restore'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


