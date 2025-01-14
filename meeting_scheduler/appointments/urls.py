from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_appointment, name='create_appointment'),
    path('select-date/<int:appointment_id>/', views.select_date, name='select_date'),
    path('dashboard/', views.dashboard, name='dashboard'),
]
