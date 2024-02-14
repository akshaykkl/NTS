from django.contrib import admin
from .models import *
# Register your models here.
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('user', 'teacher_id', 'name', 'designation', 'dept', 'hod')
    search_fields = ('name', 'designation', 'dept__dept_name')  
    list_filter = ('dept', 'hod')  # Enable filtering by department and hod status
    
    # If you have many-to-many or foreign key fields and want to make them easier to edit, consider using:
    # filter_horizontal = ('fieldname',)
    # or
    # filter_vertical = ('fieldname',)

admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Department)

'''class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'adm_no', 'name', 'year_of_admission', 'pgm', 'current_sem', 'status')
    search_fields = ('name', 'adm_no', 'name', 'pgm' )  
    list_filter = ('pgm', 'gender')

admin.site.register(Student, StudentAdmin)
'''