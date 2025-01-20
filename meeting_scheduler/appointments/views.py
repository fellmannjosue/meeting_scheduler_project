from django.shortcuts import render, redirect, get_object_or_404
from .models import Appointment, Teacher, Grade, Relationship, Schedule
from .forms import AppointmentForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from datetime import datetime, timedelta


def create_appointment(request):
    """Vista para crear una nueva cita."""
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save()
            return redirect('select_date', appointment_id=appointment.id)
    else:
        form = AppointmentForm()

    teachers = Teacher.objects.all()
    grades = Grade.objects.all()
    relationships = Relationship.objects.all()

    return render(request, 'appointments/create_appointment.html', {
        'form': form,
        'teachers': teachers,
        'grades': grades,
        'relationships': relationships,
    })


def select_date(request, appointment_id):
    """Vista para seleccionar la fecha y hora."""
    appointment = get_object_or_404(Appointment, id=appointment_id)
    teacher = appointment.teacher

    if request.method == 'POST':
        # Recoger datos del formulario
        date = request.POST.get('selected_date')
        time = request.POST.get('selected_time')
        email = request.POST.get('email')
        phone = request.POST.get('phone')

        # Verificar que los datos existen
        if date and time and email and phone:
            # Asignar los valores al objeto Appointment
            appointment.date = date
            appointment.time = time
            appointment.email = email
            appointment.phone = phone
            appointment.save()  # Guardar los datos en la base de datos
            return redirect('dashboard')
        else:
            return render(request, 'appointments/select_date.html', {
                'appointment': appointment,
                'error': 'Todos los campos son obligatorios.',
            })

    return render(request, 'appointments/select_date.html', {
        'appointment': appointment,
    })


def get_available_slots(request):
    """API para obtener horarios disponibles."""
    teacher_id = request.GET.get('teacher_id')
    date_str = request.GET.get('date')

    if not teacher_id or not date_str:
        return JsonResponse({'error': 'Parámetros inválidos'}, status=400)

    try:
        selected_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        day_of_week = selected_date.strftime('%A')

        # Filtrar horarios disponibles según el maestro y el día
        schedules = Schedule.objects.filter(teacher_id=teacher_id, day_of_week=day_of_week)
        reserved_slots = Appointment.objects.filter(teacher_id=teacher_id, date=selected_date).values_list('time', flat=True)

        available_slots = []
        for schedule in schedules:
            start_time = schedule.start_time
            end_time = schedule.end_time

            while start_time < end_time:
                if start_time not in reserved_slots:
                    available_slots.append(start_time.strftime('%H:%M'))
                start_time = (datetime.combine(datetime.today(), start_time) + timedelta(minutes=30)).time()

        return JsonResponse({'slots': available_slots})

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
def dashboard(request):
    """Vista del Dashboard para mostrar citas."""
    appointments = Appointment.objects.all().order_by('date', 'time')  # Ordenar por fecha y hora
    return render(request, 'appointments/dashboard.html', {
        'appointments': appointments,
    })
