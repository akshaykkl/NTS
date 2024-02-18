from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import Student, Teacher, Department, Programme

class StudentInline(admin.StackedInline):
    model = Student
    can_delete = False

class TeacherInline(admin.StackedInline):
    model = Teacher
    can_delete = False

class CustomUserAdmin(UserAdmin):
    inlines = (StudentInline, TeacherInline)

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Department)
admin.site.register(Programme)

class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'admn_no', 'name', 'year_of_admission', 'pgm', 'current_sem', 'status')
    search_fields = ('name', 'admn_no', 'name', 'pgm__pgm_name')  
    list_filter = ('pgm', 'gender')

    def save_model(self, request, obj, form, change):
        obj.save()
        # Create a Student instance with the associated user instance
        Student.objects.create(user=obj)

admin.site.register(Student, StudentAdmin)

class TeacherAdmin(admin.ModelAdmin):
    list_display = ('user', 'teacher_id', 'name', 'designation', 'dept', 'hod')
    search_fields = ('name', 'designation', 'dept__dept_name')  
    list_filter = ('dept', 'hod')  

    def save_model(self, request, obj, form, change):
        obj.save()
        # Create a Teacher instance with the associated user instance
        Teacher.objects.create(user=obj)

admin.site.register(Teacher, TeacherAdmin)
