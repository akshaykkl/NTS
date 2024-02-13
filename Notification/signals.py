
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.contrib.auth.models import User, Group
from .models import Student, Teacher

@receiver(m2m_changed, sender=User.groups.through)
def create_user_profile_based_on_group(sender, instance, action, pk_set, **kwargs):
    if action == "post_add":
        for pk in pk_set:
            group = Group.objects.get(pk=pk)
            if group.name == "Student":
                Student.objects.get_or_create(user=instance)
            elif group.name == "Teacher":
                Teacher.objects.get_or_create(user=instance)
