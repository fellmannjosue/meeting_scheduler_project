from django.urls import path
from . import views  # Importa las vistas de tu app

urlpatterns = [
    path('', views.index, name='menu'),  # Ruta para la página del menú
]
