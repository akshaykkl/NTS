# Generated by Django 4.2.6 on 2024-06-22 09:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Notification', '0005_student_dept_alter_student_user_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='dept',
        ),
    ]
