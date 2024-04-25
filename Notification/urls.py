from django.urls import path, include
from django.conf.urls.static import static

from .views import *
urlpatterns = [
    path('',home, name="home"),
    path('upload/', media_upload, name= 'media_upload'),
    path('view/', teacher_view, name="teacher_view"),
    path('feed/', feed, name='feed'),
    path('profile/', profile, name="profile"),
    path('change_password/', change_password, name="change_password"),
    path('password-reset/', password_reset, name='password_reset'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


