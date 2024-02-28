# utils.py

from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.urls import reverse

def send_password_reset_email(request, email):
    user = User.objects.filter(email=email).first()
    if user:
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        reset_url = request.build_absolute_uri(reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': token}))

        subject = 'Password Reset Request'
        message = render_to_string('Notification/password_reset_email.html', {
            'reset_url': reset_url,
        })
        sender = 'akkukkl10@gmail.com'  # Change this to your email address
        send_mail(subject, message, sender, [email])

        return True  # Email sent successfully
    else:
        return False  # User with provided email does not exist
