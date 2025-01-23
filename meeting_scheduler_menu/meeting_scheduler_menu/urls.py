from django.urls import path
from django.views.generic import TemplateView

urlpatterns = [
    # Carga el archivo index.html como la página principal
    path('', TemplateView.as_view(template_name='index.html'), name='menu'),
]
