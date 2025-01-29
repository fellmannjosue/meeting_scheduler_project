from django.urls import path
from django.contrib import admin
from . import views

urlpatterns = [
    # Ventana 1: Datos del usuario
    path('user-data/', views.user_data, name='user_data'),

    # Ventana 2: Motivo de la cita
    path('motivo/', views.motivo, name='motivo'),

    # Ventana 3: Selección de fecha y hora
    path('select-date/<int:appointment_id>/', views.select_date, name='select_date'),

    # API: Obtener materias por grado
    path('get-subjects-by-grade/', views.get_subjects_by_grade, name='get_subjects_by_grade'),

    # API: Obtener maestro y área por materia
    path('get-teacher-by-subject/', views.get_teacher_by_subject, name='get_teacher_by_subject'),

    # Vista del Dashboard (opcional)
    path('dashboard/', views.dashboard, name='dashboard'),

    # API: Obtener horarios disponibles

    path('get-available-slots/', views.get_available_slots, name='get_available_slots'),

    path('admin/', admin.site.urls),
]
