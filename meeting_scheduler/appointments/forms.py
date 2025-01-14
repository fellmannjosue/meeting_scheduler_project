from django import forms
from .models import Appointment

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['parent_name', 'student_name', 'grade', 'relationship', 'teacher', 'reason']
