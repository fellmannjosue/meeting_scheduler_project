from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('appointments/', include('appointments.urls')),
    path('users/', include('users.urls')),  # Asegúrate de que 'users.urls' esté correctamente referenciado
]
