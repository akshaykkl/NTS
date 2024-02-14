from django.db import models
from django.conf import settings
# Create your models here.

class Department(models.Model):
    dept_id = models.IntegerField()
    dept_name = models.CharField(max_length=100)
    def  __str__(self):
        return self.dept_name

class Programme(models.Model):
    pgm_name = models.CharField(max_length=50)
    grad_level = models.CharField(max_length=10)
    dept_id = models.ForeignKey(Department, on_delete=models.CASCADE, default=1)
    def __str__(self):
        return self.pgm_name

class Student(models.Model):
    gender_choices = [('Male','male'),
                     ('Female', 'female'),
                     ('Other', 'other')]
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)
    admn_no = models.IntegerField(unique=True)
    name = models.CharField(max_length=30)
    gender = models.CharField(max_length=10, choices=gender_choices, default='Male')
    year_of_admission = models.IntegerField()
    pgm = models.ForeignKey(Programme, on_delete=models.CASCADE, default=1)
    current_sem = models.IntegerField()
    status = models.TextField()
    def __str__(self):
        return self.name

class Teacher(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)
    teacher_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=50)
    designation = models.CharField(max_length=20)
    dept = models.ForeignKey(Department, on_delete=models.CASCADE, default=1)
    hod = models.BooleanField(default=False)
    def  __str__(self):
        return f"{self.name}"