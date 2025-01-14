from django.contrib import admin
from .models import Teacher, Schedule, Appointment,Relationship, Grade


# Configuración para el modelo Teacher
@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('name', 'area', 'class_name')


# Configuración para el modelo Schedule
@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('teacher', 'day_of_week', 'start_time', 'end_time')


# Configuración para el modelo Appointment
@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('parent_name', 'student_name', 'teacher', 'date', 'time', 'status')
    list_filter = ('status', 'teacher', 'date')
    search_fields = ('parent_name', 'student_name', 'teacher__name')

 

# Configuración para el modelo Grade
@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('name',)

# Registro para otros modelos (si no están ya registrados)
@admin.register(Relationship)
class RelationshipAdmin(admin.ModelAdmin):
    list_display = ('name',)
