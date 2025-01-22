from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from appointments.models import Appointment

def user_login(request):
    """Vista para iniciar sesión."""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Inicio de sesión exitoso.')
            return redirect('dashboard')
        else:
            messages.error(request, 'Nombre de usuario o contraseña incorrectos.')
    return render(request, 'users/login.html')

@login_required
def dashboard(request):
    """Vista para mostrar el dashboard con las citas."""
    appointments = Appointment.objects.all()
    return render(request, 'appointments/dashboard.html', {
        'appointments': appointments,
    })
