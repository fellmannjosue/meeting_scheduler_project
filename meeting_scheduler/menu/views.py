from django.shortcuts import render

def index(request):
    return render(request, 'index.html')  # Cambia 'index.html' por la plantilla que desees usar
