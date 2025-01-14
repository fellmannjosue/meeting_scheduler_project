from django.shortcuts import render, redirect, get_object_or_404
from .models import Appointment, Teacher
from .forms import AppointmentForm
from django.contrib.auth.decorators import login_required

def create_appointment(request):
    """Vista para crear una nueva cita"""
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            teacher = form.cleaned_data['teacher']
            # Determinar el área automáticamente
            appointment.area = teacher.area if teacher.area != 'Asociado' else teacher.class_name
            appointment.save()
            return redirect('select_date', appointment_id=appointment.id)
    else:
        form = AppointmentForm()

    return render(request, 'appointments/create_appointment.html', {'form': form})

def select_date(request, appointment_id):
    """Vista para seleccionar la fecha y hora de la cita"""
    appointment = get_object_or_404(Appointment, id=appointment_id)
    if request.method == 'POST':
        date = request.POST.get('date')
        time = request.POST.get('time')
        if date and time:
            appointment.date = date
            appointment.time = time
            appointment.save()
            return redirect('dashboard')

    return render(request, 'appointments/select_date.html', {'appointment': appointment})

@login_required
def dashboard(request):
    """Vista para el dashboard de las citas"""
    appointments = Appointment.objects.all().order_by('date', 'time')
    return render(request, 'appointments/dashboard.html', {'appointments': appointments})
