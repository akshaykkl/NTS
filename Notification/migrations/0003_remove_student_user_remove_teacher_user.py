# Generated by Django 4.2.6 on 2024-02-12 18:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Notification', '0002_department_student_user_teacher_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='user',
        ),
        migrations.RemoveField(
            model_name='teacher',
            name='user',
        ),
    ]
