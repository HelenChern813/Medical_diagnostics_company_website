from django import forms
from django.utils import timezone

from .models import Appointment, Doctors, Services, Feedback


class AppointmentForm(forms.ModelForm):
    doctor = forms.ModelChoiceField(queryset=Doctors.objects.all(), label="Врач", required=True)

    class Meta:
        model = Appointment
        fields = ["doctor", "service", "appointment_date", "notes"]
        widgets = {
            "appointment_date": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "notes": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        if user:
            # Динамически фильтруем услуги по выбранному врачу
            self.fields["service"].queryset = Services.objects.none()

            if "doctor" in self.data:
                try:
                    doctor_id = int(self.data.get("doctor"))
                    self.fields["service"].queryset = Services.objects.filter(
                        doctor_id=doctor_id, is_active=True
                    ).order_by("name")
                except (ValueError, TypeError):
                    pass
            elif self.instance.pk:
                self.fields["service"].queryset = self.instance.service.doctor.services_set.filter(
                    is_active=True
                ).order_by("name")

        self.fields["appointment_date"].input_formats = ["%Y-%m-%dT%H:%M"]

    def clean_appointment_date(self):
        appointment_date = self.cleaned_data["appointment_date"]

        if appointment_date < timezone.now():
            raise forms.ValidationError("Нельзя записаться на прошедшую дату!")

        return appointment_date


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['name', 'email', 'phone', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }
        labels = {
            'name': 'Ваше имя',
            'email': 'Email для ответа',
            'phone': 'Контактный телефон',
            'message': 'Ваше сообщение',
        }
