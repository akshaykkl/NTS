# Generated by Django 4.2.6 on 2024-02-08 08:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_id', models.IntegerField()),
                ('name', models.CharField(max_length=30)),
                ('year_of_admission', models.IntegerField()),
                ('admission_no', models.IntegerField()),
                ('current_sem', models.IntegerField()),
                ('status', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('teacher_id', models.IntegerField()),
                ('name', models.CharField(max_length=50)),
                ('designation', models.CharField(max_length=20)),
                ('hod', models.BooleanField()),
            ],
        ),
    ]
