from django.db import models


class Relationship(models.Model):
    name = models.CharField(max_length=50)  # Tipo de parentesco (padre, madre, tutor, etc.)

    def __str__(self):
        return self.name


class Grade(models.Model):
    name = models.CharField(max_length=50)  # Nombre del grado (Primero, Segundo, etc.)

    def __str__(self):
        return self.name


class Teacher(models.Model):
    name = models.CharField(max_length=255)  # Nombre del maestro
    area = models.CharField(
        max_length=50,
        choices=[
            ('Preescolar', 'Preescolar'),
            ('Primaria', 'Primaria'),
            ('Secundaria', 'Secundaria'),
            ('Asociado', 'Asociado'),
        ]
    )
    class_name = models.CharField(max_length=255, null=True, blank=True)  # Clase impartida (solo para Asociado)

    def __str__(self):
        return self.name


class Schedule(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name="schedules")
    day_of_week = models.CharField(
        max_length=10,
        choices=[
            ('Monday', 'Lunes'),
            ('Tuesday', 'Martes'),
            ('Wednesday', 'Miércoles'),
            ('Thursday', 'Jueves'),
            ('Friday', 'Viernes'),
            ('Saturday', 'Sábado'),
            ('Sunday', 'Domingo'),
        ]
    )
    start_time = models.TimeField()  # Hora de inicio
    end_time = models.TimeField()  # Hora de fin

    def __str__(self):
        return f"{self.teacher.name} - {self.day_of_week} ({self.start_time} - {self.end_time})"


class Appointment(models.Model):
    parent_name = models.CharField(max_length=255)  # Nombre del padre
    student_name = models.CharField(max_length=255)  # Nombre del alumno
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE)  # Grado del alumno
    relationship = models.ForeignKey(Relationship, on_delete=models.CASCADE)  # Parentesco
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)  # Maestro seleccionado
    area = models.CharField(max_length=50)  # Área
    reason = models.TextField()  # Razón o motivo de la cita
    date = models.DateField(null=True, blank=True)  # Fecha de la cita
    time = models.TimeField(null=True, blank=True)  # Hora de la cita
    status = models.CharField(
        max_length=50,
        choices=[
            ('Pendiente', 'Pendiente'),
            ('Confirmada', 'Confirmada'),
            ('Cancelada', 'Cancelada'),
        ],
        default='Pendiente'
    )  # Estado de la cita

    def __str__(self):
        return f"{self.parent_name} - {self.teacher.name} ({self.date} {self.time})"
