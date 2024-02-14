# Generated by Django 4.1.5 on 2024-02-14 05:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Notification", "0007_rename_pgm_id_student_pgm_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="student",
            name="admn_no",
            field=models.IntegerField(unique=True),
        ),
        migrations.AlterField(
            model_name="teacher",
            name="hod",
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name="teacher",
            name="teacher_id",
            field=models.IntegerField(unique=True),
        ),
    ]
