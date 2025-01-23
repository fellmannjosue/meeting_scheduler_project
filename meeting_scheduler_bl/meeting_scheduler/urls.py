from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('appointments_col/', include('appointments_col.urls')),
    path('users_col/', include('users_col.urls')),  
    path('appointments_bl/', include('appointments_bl.urls')),
    path('users_bl/', include('users_bl.urls')),
]
