from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Appointment, Teacher, Grade, Subject, Relationship, Schedule
from .forms import AppointmentForm
from datetime import datetime, timedelta


def user_data(request):
    """Primera ventana: captura de datos del usuario."""
    if request.method == 'POST':
        parent_name = request.POST.get('parent_name')
        student_name = request.POST.get('student_name')
        relationship_id = request.POST.get('relationship')

        if parent_name and student_name and relationship_id:
            # Guardar los datos en sesión
            request.session['parent_name'] = parent_name
            request.session['student_name'] = student_name
            request.session['relationship_id'] = relationship_id
            return redirect('motivo')
        else:
            return render(request, 'appointments_col/user_data.html', {
                'error': 'Por favor, complete todos los campos.',
                'relationships': Relationship.objects.all(),
            })

    return render(request, 'appointments_col/user_data.html', {
        'relationships': Relationship.objects.all(),
    })


def motivo(request):
    """Segunda ventana: selección del motivo y detalles."""
    if request.method == 'POST':
        # Obtener datos desde el formulario
        grade_id = request.POST.get('grade')
        subject_id = request.POST.get('subject')
        reason = request.POST.get('reason')

        # Verificar que los datos requeridos estén presentes
        if grade_id and subject_id and reason:
            # Obtener los datos de la sesión
            parent_name = request.session.get('parent_name')
            student_name = request.session.get('student_name')
            relationship_id = request.session.get('relationship_id')

            # Verificar que los datos requeridos de la sesión estén disponibles
            if not all([parent_name, student_name, relationship_id]):
                return JsonResponse({'error': 'Faltan datos del usuario. Por favor, regrese al paso anterior.'}, status=400)

            # Obtener el objeto de la materia
            try:
                subject = Subject.objects.get(id=subject_id)
            except Subject.DoesNotExist:
                return JsonResponse({'error': 'La materia seleccionada no existe.'}, status=400)

            # Crear la cita
            appointment = Appointment.objects.create(
                parent_name=parent_name,
                student_name=student_name,
                relationship_id=relationship_id,
                grade_id=grade_id,
                subject=subject,
                teacher=subject.teacher,
                area=subject.teacher.area,
                reason=reason
            )

            # Devolver el ID de la cita como respuesta JSON
            return JsonResponse({'appointment_id': appointment.id}, status=200)

        # Si faltan datos en el formulario
        return JsonResponse({'error': 'Por favor, complete todos los campos del formulario.'}, status=400)

    # Para solicitudes GET, renderizar el HTML
    return render(request, 'appointments_col/motivo.html', {
        'grades': Grade.objects.all(),
    })




def select_date(request, appointment_id):
    """Tercera ventana: selección de fecha y hora."""
    appointment = get_object_or_404(Appointment, id=appointment_id)

    if request.method == 'POST':
        date = request.POST.get('selected_date')
        time = request.POST.get('selected_time')
        email = request.POST.get('email')
        phone = request.POST.get('phone')

        if date and time and email and phone:
            # Actualizar la cita con los datos finales
            appointment.date = date
            appointment.time = time
            appointment.email = email
            appointment.phone = phone
            appointment.save()
            return redirect('dashboard')
        else:
            return render(request, 'appointments/select-date.html', {
                'error': 'Todos los campos son obligatorios.',
                'appointment': appointment,
            })

    return render(request, 'appointments_col/select-date.html', {
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

        # Obtener los horarios del maestro en el día de la semana especificado
        schedules = Schedule.objects.filter(teacher_id=teacher_id, day_of_week=day_of_week)
        # Obtener horarios ya reservados
        reserved_slots = Appointment.objects.filter(teacher_id=teacher_id, date=selected_date).values_list('time', flat=True)

        available_slots = []
        for schedule in schedules:
            start_time = schedule.start_time
            end_time = schedule.end_time

            while start_time < end_time:
                next_time = (datetime.combine(datetime.today(), start_time) + timedelta(minutes=30)).time()
                slot_range = f"{start_time.strftime('%H:%M')}-{next_time.strftime('%H:%M')}"
                if start_time not in reserved_slots:
                    available_slots.append({'time': slot_range, 'available': True})
                else:
                    available_slots.append({'time': slot_range, 'available': False})
                start_time = next_time

        return JsonResponse({'slots': available_slots})

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
def dashboard(request):
    """Vista del Dashboard para mostrar citas."""
    appointments = Appointment.objects.all().order_by('date', 'time')
    return render(request, 'appointments_col/dashboard.html', {
        'appointments': appointments,
    })


def get_subjects_by_grade(request):
    """API para obtener las materias relacionadas con un grado."""
    grade_id = request.GET.get('grade_id')
    if not grade_id:
        return JsonResponse({'error': 'Grado no proporcionado'}, status=400)

    try:
        subjects = Subject.objects.filter(grade_id=grade_id)
        data = [{'id': subject.id, 'name': subject.name} for subject in subjects]
        return JsonResponse({'subjects': data})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def get_teacher_by_subject(request):
    """API para obtener el maestro y el área relacionada con una materia."""
    subject_id = request.GET.get('subject_id')
    if not subject_id:
        return JsonResponse({'error': 'Materia no proporcionada'}, status=400)

    try:
        subject = Subject.objects.get(id=subject_id)
        teacher = subject.teacher
        data = {
            'teacher': {
                'id': teacher.id,
                'name': teacher.name,
                'area': teacher.area,
            }
        }
        return JsonResponse(data)
    except Subject.DoesNotExist:
        return JsonResponse({'error': 'Materia no encontrada'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
