from django.db import models
from django.conf import settings
from django.utils import timezone
# Create your models here.

class Department(models.Model):
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
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
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
        ('AssistantProfessor','Assistant Professor'),
        ('associateProfessor','Associate Professor'),
        ('Professor','Professor'),
        ('GuestLecturer','Guest Lecturer'),
        ('Principal','Principal')]
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
        ('archive', 'Archive'),
        ('upload', 'Upload'),
    )
    MEDIA_CATEGORY = (
    ('Examination','Examination'),
    ('Eepartment', 'Department'),
    ('Notice','Notice'),
    ('Order','Order'),
    )
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    media_type = models.CharField(max_length=20, choices=MEDIA_TYPES, null=True, blank=True)
    file = models.FileField(upload_to='media_files/',null=True, blank=True)
    media_category = models.CharField(max_length=50, choices=MEDIA_CATEGORY,null=True, blank=True)
    dept = models.ForeignKey(Department, on_delete=models.CASCADE,null=True, blank=True)
    student = models.BooleanField(default=False)
    teacher = models.BooleanField(default=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now, editable=False)

    def __str__(self):
        return self.title
    
    def move_to_trash(self, user):
        TrashMedia.objects.create(
            title=self.title,
            description=self.description,
            media_type=self.media_type,
            file=self.file,
            media_category=self.media_category,
            dept=self.dept,
            student=self.student,
            teacher=self.teacher,
            created_at=self.created_at,
            created_by=self.created_by,
            trashed_by=user,
        )
        self.delete()


class TrashMedia(models.Model):
    MEDIA_TYPES = (
        ('archive', 'Archive'),
        ('upload', 'Uploads'),
    )
    MEDIA_CATEGORY = (
    ('Examination','Examination'),
    ('Department', 'Department'),
    ('Notice','Notics'),
    ('Order','Order'),
    )
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    media_type = models.CharField(max_length=20, choices=MEDIA_TYPES, null=True, blank=True)
    file = models.FileField(upload_to='media_files/',null=True, blank=True)
    media_category = models.CharField(max_length=50, choices=MEDIA_CATEGORY,null=True, blank=True)
    dept = models.ForeignKey(Department, on_delete=models.CASCADE,null=True, blank=True)
    student = models.BooleanField(default=False)
    teacher = models.BooleanField(default=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_trashmedia_set')
    created_at = models.DateTimeField()
    trashed_at = models.DateTimeField(default=timezone.now, editable=False)
    trashed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='trashed_trashmedia_set', null=True)

    def __str__(self):
        return self.title

    def restore(self):
        Media.objects.create(
            title=self.title,
            description=self.description,
            media_type=self.media_type,
            file=self.file,
            media_category=self.media_category,
            dept=self.dept,
            student=self.student,
            teacher=self.teacher,
            created_at=self.created_at,
            created_by=self.created_by,
        )
        self.delete()