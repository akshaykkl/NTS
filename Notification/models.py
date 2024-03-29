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
    gender_choices = [('male', 'Male'),
                     ('female', 'Female'),
                     ('other', 'Other')]
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)
    admn_no = models.IntegerField(unique=True)
    name = models.CharField(max_length=30)
    gender = models.CharField(max_length=10, choices=gender_choices)
    year_of_admission = models.IntegerField()
    pgm = models.ForeignKey(Programme, on_delete=models.CASCADE)
    current_sem = models.IntegerField()
    status = models.TextField()
    def __str__(self):
        return self.name

class Teacher(models.Model):
    design = [
        ('assistantProfessor','Assistant Professor'),
        ('associateProfessor','Associate Professor'),
        ('Professor','Professor'),
        ('guestLecturer','Guest Lecturer'),
        ('principal','Principal')]
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    teacher_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=50)
    designation = models.CharField(max_length=20, choices=design)
    dept = models.ForeignKey(Department, on_delete=models.CASCADE)
    hod = models.BooleanField(default=False)
    def  __str__(self):
        return f"{self.name}"
    


class Media(models.Model):
    MEDIA_TYPES = (
        ('image', 'Image'),
        ('video', 'Video'),
        ('audio', 'Audio'),
        ('document', 'Document'),
        # Add more types as needed
    )

    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    media_type = models.CharField(max_length=20, choices=MEDIA_TYPES, null=True, blank=True)
    file = models.FileField(upload_to='media_files/',null=True, blank=True)
    pgm = models.ForeignKey(Programme, on_delete=models.CASCADE)
    student = models.BooleanField(default=False)
    teacher = models.BooleanField(default=False)
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
